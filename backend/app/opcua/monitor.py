# backend/app/opcua/monitor.py

import asyncio
from datetime import datetime
from app.opcua.connector import OPCUAConnector
from app.db.models.server import OPCServer
from app.db.models.tag import Tag
from app.db.database import SessionLocal
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)


async def poll_server_tags(server: OPCServer, tags: list[Tag]):
    connector = OPCUAConnector(server.endpoint_url)
    await connector.connect()

    try:
        tag_nodes = {tag.alias or tag.node_id: tag.node_id for tag in tags}
        result = await connector.read_values(list(tag_nodes.values()))

        for tag, value in zip(tags, result):
            logger.info(f"[{server.name}] {tag.alias or tag.node_id}: {value}")

            # Future hook: Save to Influx/Postgres or trigger alerts
            # await save_to_timeseries_db(server, tag, value)

    except Exception as e:
        logger.error(f"Polling failed for server {server.name}: {e}")
    finally:
        await connector.disconnect()


async def monitor_loop(interval_seconds=10):
    while True:
        logger.info("Polling all configured OPC UA servers...")
        db = SessionLocal()
        try:
            servers = db.query(OPCServer).options(joinedload(OPCServer.tags)).all()
            for server in servers:
                tags = server.tags
                if tags:
                    asyncio.create_task(poll_server_tags(server, tags))
        except Exception as e:
            logger.error(f"Error during monitoring loop: {e}")
        finally:
            db.close()

        await asyncio.sleep(interval_seconds)
