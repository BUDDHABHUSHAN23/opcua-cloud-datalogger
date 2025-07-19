# app/services/engine_control.py

import logging
from app.services.monitor import stop_monitoring_task
from app.services.scheduler import stop_all_schedulers, reload_schedulers

logger = logging.getLogger("engine-control")

async def shutdown_engine():
    logger.info("Stopping all background tasks...")
    await stop_monitoring_task()
    await stop_all_schedulers()
    logger.info("Shutdown complete.")

async def reload_engine():
    logger.info("Reloading configuration and restarting tasks...")
    await stop_monitoring_task()
    await stop_all_schedulers()
    await reload_schedulers()
    logger.info("Reload complete.")
