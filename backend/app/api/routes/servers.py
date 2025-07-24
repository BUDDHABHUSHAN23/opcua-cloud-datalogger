from fastapi import APIRouter, Depends, HTTPException   #To create the end point and handle dependencies 
from sqlalchemy.orm import Session    # To handle database sessions 
from typing import List   # To define a list of servers
from app.db.models.group import Group   

from app.db.database import get_db
from app.db.models.server import Server
from app.schemas.server import ServerCreate, ServerOut
from app.db.crud import server as crud
from app.opcua.connector import OPCUAConnector

router = APIRouter()    # Used in the modular routing system of FastAPI & for better organization of the code with defining sub-routes

@router.get("/", response_model=List[ServerOut])   # To get a list of all servers
def list_servers(db: Session = Depends(get_db)):   # Dependency injection to get the database session they are present in the database
    try:
        return crud.get_all_servers(db)            # Get all servers from the database 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))      # Handle any exceptions that occur during the retrieval of servers

@router.post("/", response_model=ServerOut, status_code=201)
def create_server(server: ServerCreate, db: Session = Depends(get_db)):   # To create a new server  
    try:
        return crud.add_server(db, server.name, server.endpoint_url)      # Add a new server to the database
    except Exception as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail=str(e))           # If a server with the same name or endpoint already exists, raise a conflict error
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{server_id}", status_code=200)                           
def remove_server(server_id: int, db: Session = Depends(get_db)):
    try:
        # Check if server exists
        server = db.query(Server).filter(Server.id == server_id).first()
        if not server:
            raise HTTPException(status_code=404, detail="Server not found")

        # Check if any groups are linked to this server
        group_count = db.query(Group).filter(Group.server_id == server_id).count()    # Count the number of groups linked to this server count() is used to get the number of groups linked to this server
        if group_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete server {server_id}: {group_count} group(s) are still linked to it."  
            )
 
        crud.delete_server(db, server_id)             # Delete the server from the database
        return {"detail": f"Server {server_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{server_id}/browse")
async def browse_server(server_id: int, db: Session = Depends(get_db)):   # To browse the root nodes of a server
    server = crud.get_server_by_id(db, server_id)                         # Get the server by its ID from the database
    try:
        connector = OPCUAConnector(server.endpoint_url)   # Create an OPCUAConnector instance with the server's endpoint URL
        await connector.connect()                         # Connect to the OPC UA server
        nodes = await connector.browse_root()             # Browse the root nodes of the server through which it connected
        await connector.disconnect()                      # Disconnect from the OPC UA server
        return {"root_nodes": nodes}                      # Return the list of root nodes found in the server
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/{server_id}/browse/{node_id}")
async def browse_node(server_id: int, node_id: str, db: Session = Depends(get_db)):
    server = crud.get_server_by_id(db, server_id)
    try:
        if node_id.isdigit():
            node_id = f"i={node_id}"

        connector = OPCUAConnector(server.endpoint_url)
        await connector.connect()
        node = connector.client.get_node(node_id)
        children = await node.get_children()
        result = []
        for child in children:
            display_name = await child.read_display_name()
            result.append({
                "nodeId": child.nodeid.to_string(),
                "displayName": str(display_name),
                "type": str(await child.read_node_class())
            })
        await connector.disconnect()
        return {"children": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Browse failed: {e}")
