# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from app.websocket.live_updates import manager
# import asyncio

# router = APIRouter()

# @router.websocket("/ws/live")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             await asyncio.sleep(60)  # Keep alive; no receive needed
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
