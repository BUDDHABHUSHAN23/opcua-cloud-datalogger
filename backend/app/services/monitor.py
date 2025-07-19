# app/services/monitor.py

import asyncio
import logging

logger = logging.getLogger("monitor-service")

monitor_task = None

async def start_monitoring_task():
    global monitor_task
    if monitor_task and not monitor_task.done():
        logger.info("Monitor task already running.")
        return

    async def monitor_loop():
        logger.info("Starting monitor loop...")
        while True:
            # TODO: Poll tags or listen to changes
            await asyncio.sleep(5)

    monitor_task = asyncio.create_task(monitor_loop())


async def stop_monitoring_task():
    global monitor_task
    if monitor_task:
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            logger.info("Monitor task cancelled.")
        monitor_task = None
