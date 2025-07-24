from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError
from app.services.auth import SECRET_KEY, ALGORITHM
from app.websocket.live_updates import manager

router = APIRouter()

@router.websocket("/ws/live")
async def websocket_live(websocket: WebSocket, token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub", "unknown")
        print(f"[Live WS] Connected user: {user_email}")

        await manager.connect(websocket)

        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("[Live WS] Disconnected")
    except JWTError:
        await websocket.close(code=1008)
        print("[Live WS] Invalid token")
    except Exception as e:
        print(f"[Live WS] Error: {e}")
        await websocket.close()
