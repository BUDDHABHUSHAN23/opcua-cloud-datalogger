# app/workers/monitor_worker.py

from celery_app import celery
from app.opcua.connector import get_opcua_client
from app.services.influx_writer import write_tag_value
from app.db.database import SessionLocal
from app.db.models.tag import Tag
from asyncua import ua
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task
def monitor_tags():
    logger.info("Starting tag monitoring task")

    db = SessionLocal()
    tags = db.query(Tag).all()
    db.close()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_tags(tags))
    loop.close()

async def process_tags(tags):
    server_tags = {}
    for tag in tags:
        server_tags.setdefault(tag.server_id, []).append(tag)

    for server_id, tag_list in server_tags.items():
        client = await get_opcua_client(server_id)
        if not client:
            continue

        try:
            async with client:
                for tag in tag_list:
                    try:
                        node = client.get_node(tag.node_id)
                        val = await node.read_value()
                        logger.info(f"Tag {tag.alias} = {val}")
                        await write_tag_value(
                            server_name=str(server_id),
                            tag_name=tag.alias,
                            value=val,
                            timestamp=None
                        )
                    except Exception as e:
                        logger.error(f"Failed reading tag {tag.alias}: {e}")
        except Exception as e:
            logger.error(f"Client error for server {server_id}: {e}")
