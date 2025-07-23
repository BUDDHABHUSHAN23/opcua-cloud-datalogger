# app/api/routes/ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from asyncua import Client
from typing import List
import asyncio
import logging
from jose import jwt, JWTError
from app.services.auth import SECRET_KEY, ALGORITHM

router = APIRouter()
logger = logging.getLogger("websocket-monitor")

@router.websocket("/monitor")
async def websocket_monitor(websocket: WebSocket, token: str = Query(...)):
    try:
        # 🔐 Token decode
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")  # Optional: get user info
        logger.info(f"WebSocket connected for user: {user_email}")

        await websocket.accept()

        # 📥 Receive initial payload with server_url and node_ids
        init_data = await websocket.receive_json()
        server_url = init_data.get("server_url")
        node_ids: List[str] = init_data.get("node_ids", [])

        if not server_url or not node_ids:
            await websocket.send_json({"error": "Missing server_url or node_ids"})
            await websocket.close()
            return
        
        print(f"Incoming token: {token}")
        print(f"Connecting to server: {server_url} with nodes: {node_ids}")

        async with Client(url=server_url) as client:
            while True:
                updates = []
                for node_id in node_ids:
                    try:
                        node = client.get_node(node_id)
                        data_value = await node.read_data_value()
                        updates.append({
                            "nodeId": node_id,
                            "value": str(data_value.Value.Value),
                            "quality": data_value.StatusCode.name,
                            "timestamp": str(data_value.SourceTimestamp),
                        })
                    except Exception as e:
                        updates.append({
                            "nodeId": node_id,
                            "value": None,
                            "quality": "ReadError",
                            "error": str(e)
                        })

                await websocket.send_json({"values": updates})
                await asyncio.sleep(5)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except JWTError:
        logger.warning("Invalid WebSocket token")
        await websocket.close(code=1008)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()
