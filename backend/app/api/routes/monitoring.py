# app/api/routes/monitoring.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.db.database import SessionLocal
from app.db.models.tag import Tag
from app.opcua.connector import OPCUAConnector
import asyncio
from datetime import datetime

router = APIRouter()

@router.websocket("/ws/monitor")
async def monitor_tags(websocket: WebSocket):
    await websocket.accept()
    db = SessionLocal()
    try:
        # Get all active tags with associated server
        tags = db.query(Tag).filter(Tag.server_id.isnot(None)).all()
        if not tags:
            await websocket.send_json({"error": "No tags configured"})
            return

        # Group tags by server
        tags_by_server = {}
        for tag in tags:
            if tag.server_id not in tags_by_server:
                tags_by_server[tag.server_id] = []
            tags_by_server[tag.server_id].append(tag)

        # Maintain a dict of server_id → OPCUAConnector
        connectors = {}
        for server_id in tags_by_server:
            server_url = tags_by_server[server_id][0].server.endpoint_url
            connector = OPCUAConnector(server_url)
            await connector.connect()
            connectors[server_id] = connector

        while True:
            result_payload = {
                "timestamp": datetime.utcnow().isoformat(),
                "values": []
            }
            for server_id, tag_list in tags_by_server.items():
                connector = connectors[server_id]
                node_ids = [tag.node_id for tag in tag_list]
                aliases = [tag.alias for tag in tag_list]

                values = await connector.read_values(node_ids)
                for alias, val in zip(aliases, values):
                    result_payload["values"].append({
                        "alias": alias,
                        "value": val.Value.Value,
                        "quality": val.StatusCode.name
                    })

            await websocket.send_json(result_payload)
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print("WebSocket disconnected.")
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        for conn in connectors.values():
            await conn.disconnect()
        db.close()
