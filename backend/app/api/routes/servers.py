# backend/app/api/routes/servers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.opcua.connector import OPCUAConnector

from app.db.database import SessionLocal
from app.db.crud import server as crud  # Adjust import based on your project structure
from app.db.models.server import Server  # Ensure this model is defined
from app.schemas.server import ServerCreate, ServerOut  # Make sure these are defined
from app.db.database import get_db   # Adjust import based on your project structure
 

from app.db.crud import server as server_crud


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ServerOut])
def list_servers(db: Session = Depends(get_db)):
    """List all OPC UA servers"""
    try:
        servers = db.query(Server).all()
        return servers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ServerOut)
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    """Create new OPC UA server"""
    try:
        return crud.add_server(db, server.name, server.endpoint_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{server_id}")
def remove_server(server_id: int, db: Session = Depends(get_db)):
    """Delete server by ID"""
    crud.delete_server(db, server_id)
    return {"detail": "Server deleted"}

@router.get("/{server_id}/browse")
async def browse_server(server_id: int, db: Session = Depends(get_db)):
    server = server_crud.get_server_by_id(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    try:
        connector = OPCUAConnector(server.endpoint_url)
        await connector.connect()
        nodes = await connector.browse_root()
        await connector.disconnect()
        # return {"nodes": nodes}
        print("[OPCUA] Browsed nodes:", nodes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/{server_id}/browse/{node_id}")
async def browse_node(server_id: int, node_id: str, db: Session = Depends(get_db)):
    """Browse children of a given node"""
    server = server_crud.get_server_by_id(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    try:
        # Normalize nodeId format
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
                "displayName": str(display_name)
            })
        await connector.disconnect()
        return {"children": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Browse failed: {e}")



