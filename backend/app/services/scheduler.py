# Background scheduling
# app/services/scheduler.py

import logging

logger = logging.getLogger("scheduler-service")

schedulers = []

async def stop_all_schedulers():
    global schedulers
    for task in schedulers:
        if not task.done():
            task.cancel()
            try:
                await task
            except Exception:
                pass
    schedulers = []
    logger.info("All scheduled tasks stopped.")


async def reload_schedulers():
    await stop_all_schedulers()
    # TODO: Load groups and recreate schedules
    logger.info("Reloaded all schedules (placeholder).")
