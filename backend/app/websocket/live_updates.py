# WebSocket live updates
from fastapi import WebSocket, WebSocketDisconnect
from app.db.database import SessionLocal
from app.db.crud import group as group_crud, tag as tag_crud
from app.services.opc_client import get_opc_client
import asyncio
from collections import defaultdict
from datetime import datetime
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def live_data_publisher():
    while True:
        db = SessionLocal()
        enabled_groups = [g for g in group_crud.get_all_groups(db) if g.is_enabled]
        server_tag_map = defaultdict(list)
        for group in enabled_groups:
            tags = tag_crud.get_tags_for_group(db, group.id)
            for tag in tags:
                server_tag_map[group.server_id].append((group.name, tag))
        all_data = []
        for server_id, entries in server_tag_map.items():
            client = await get_opc_client(server_id)
            if not client:
                continue
            for group_name, tag in entries:
                try:
                    node = client.get_node(tag.node_id)
                    value = await node.read_data_value()
                    all_data.append({
                        "tag": tag.alias or tag.node_id,
                        "value": str(value.Value.Value),
                        "status": value.StatusCode.name,
                        "group": group_name,
                        "timestamp": datetime.now().isoformat()
                    })
                except Exception as e:
                    all_data.append({
                        "tag": tag.alias or tag.node_id,
                        "value": "Error",
                        "status": str(e),
                        "group": group_name,
                        "timestamp": datetime.now().isoformat()
                    })
        db.close()
        await manager.broadcast(json.dumps(all_data))
        await asyncio.sleep(5)