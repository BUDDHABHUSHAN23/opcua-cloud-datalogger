# app/workers/monitor_worker.py

from celery_app import celery
from app.opcua.connector import get_opcua_client
from app.db.database import SessionLocal
from app.db.models.tag import Tag
from app.services.influx_writer import log_data_to_influx
from asyncua import ua
import asyncio
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task
def monitor_tags():
    logger.info("🟢 Starting tag monitoring task")

    db = SessionLocal()
    tags = db.query(Tag).filter(Tag.enabled == True).all()
    db.close()

    if not tags:
        logger.warning("⚠️ No enabled tags found.")
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(poll_and_write(tags))
    loop.close()

async def poll_and_write(tags):
    grouped = {}
    for tag in tags:
        grouped.setdefault(tag.server_id, []).append(tag)

    for server_id, tag_list in grouped.items():
        client = await get_opcua_client(server_id)
        if not client:
            logger.error(f"❌ Failed to get OPC client for server {server_id}")
            continue

        try:
            async with client:
                records = []
                for tag in tag_list:
                    try:
                        node = client.get_node(tag.node_id)
                        value = await node.read_value()
                        logger.info(f"🔄 {tag.alias} = {value}")

                        record = {
                            "measurement": "opc_tag",
                            "tags": {
                                "alias": tag.alias,
                                "node_id": tag.node_id,
                                "group": str(tag.group_id)
                            },
                            "fields": {
                                "value": float(value)
                            },
                            "time": datetime.utcnow()
                        }
                        records.append(record)
                    except Exception as e:
                        logger.warning(f"⚠️ Read failed for {tag.alias}: {e}")
                
                # ✅ Write to Influx
                await log_data_to_influx(records)

        except Exception as e:
            logger.error(f"❌ Client error for server {server_id}: {e}")
