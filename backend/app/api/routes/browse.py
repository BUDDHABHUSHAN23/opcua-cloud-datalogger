# app/api/routes/browse.py

from fastapi import APIRouter, HTTPException
from asyncua import Client, ua
from app.db.database import get_db
from app.db.models.server import Server
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List, Dict
import logging

router = APIRouter()

logger = logging.getLogger("browse")

# Dependency to get DB session
def get_server(db: Session, server_id: int):
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@router.get("/servers/{server_id}/browse/{node_id}", response_model=List[Dict[str, str]])
async def browse_node(server_id: int, node_id: str, db: Session = Depends(get_db)):
    server = get_server(db, server_id)
    url = server.endpoint_url

    try:
        async with Client(url=url) as client:
            node = client.get_node(node_id)
            children = await node.get_children()

            result = []
            for child in children:
                display_name = await child.read_display_name()
                result.append({
                    "nodeId": child.nodeid.to_string(),
                    "displayName": display_name.Text
                })
            return result

    except Exception as e:
        logger.exception(f"Failed to browse node {node_id} for server {server_id}")
        raise HTTPException(status_code=500, detail=str(e))
