from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models.server import Server
from app.schemas.server import ServerCreate, ServerOut
from app.db.crud import server as crud
from app.opcua.connector import OPCUAConnector

router = APIRouter()

@router.get("/", response_model=List[ServerOut])
def list_servers(db: Session = Depends(get_db)):
    try:
        return crud.get_all_servers(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ServerOut, status_code=201)
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    try:
        return crud.add_server(db, server.name, server.endpoint_url)
    except Exception as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{server_id}", status_code=200)
def remove_server(server_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_server(db, server_id)
        return {"detail": f"Server {server_id} deleted successfully"}
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{server_id}/browse")
async def browse_server(server_id: int, db: Session = Depends(get_db)):
    server = crud.get_server_by_id(db, server_id)
    try:
        connector = OPCUAConnector(server.endpoint_url)
        await connector.connect()
        nodes = await connector.browse_root()
        await connector.disconnect()
        return {"root_nodes": nodes}
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
                "displayName": str(display_name)
            })
        await connector.disconnect()
        return {"children": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Browse failed: {e}")
