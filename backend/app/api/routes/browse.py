# app/api/routes/browse.py

from fastapi import APIRouter, HTTPException
from asyncua import Client, ua
from app.db.database import get_db
from app.db.models.server import Server
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List, Dict
import logging
from app.db import crud
from app.opcua.connector import OPCUAConnector

router = APIRouter()

logger = logging.getLogger("browse")

# Dependency to get DB session
def get_server(db: Session, server_id: int):
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

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
