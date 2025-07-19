# app/api/routes/control.py

from fastapi import APIRouter
import asyncio
import logging

from app.services.engine_control import shutdown_engine, reload_engine

router = APIRouter()
logger = logging.getLogger("control")


@router.post("/shutdown")
async def shutdown_tasks():
    try:
        await shutdown_engine()
        return {"detail": "All background tasks stopped."}
    except Exception as e:
        logger.error(f"Shutdown failed: {e}")
        return {"error": str(e)}


@router.post("/reload")
async def reload_tasks():
    try:
        await reload_engine()
        return {"detail": "Configuration and tasks reloaded."}
    except Exception as e:
        logger.error(f"Reload failed: {e}")
        return {"error": str(e)}