# monitoring route
from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_monitor_status():
    return {"status": "OK", "message": "Live monitoring service running."}