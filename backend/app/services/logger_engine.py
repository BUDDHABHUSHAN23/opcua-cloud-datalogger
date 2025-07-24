import asyncio
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from app.services.opc_client import get_opc_client
from app.db.crud import group as group_crud, tag as tag_crud, log as log_crud
from app.db.database import SessionLocal
from app.services.influx_writer import log_data_to_influx  # ✅ Add at top

logging.basicConfig(level=logging.INFO)

class LoggerEngine:
    def __init__(self):
        self.running = True
        self.scheduled_tasks = {}

    async def reload_config(self):
        db = SessionLocal()
        try:
            logging.info("Reloading configuration...")
            groups = [g for g in group_crud.get_all_groups(db) if g.is_enabled]
            for group in groups:
                task = asyncio.create_task(self.schedule_group(group))
                self.scheduled_tasks[group.id] = task
        finally:
            db.close()

    async def schedule_group(self, group):
        schedule_type = group.schedule_type
        if schedule_type == "On Interval":
            await self._interval_runner(group)
        elif schedule_type == "On the Clock":
            await self._clock_runner(group)
        elif schedule_type == "On Specific Date/Time":
            await self._specific_runner(group)

    async def _interval_runner(self, group):
        interval = int(group.schedule_details)
        db = SessionLocal()
        tags = tag_crud.get_tags_for_group(db, group.id)
        db.close()
        while self.running:
            await self._log_tags(group, tags)
            await asyncio.sleep(interval)

    async def _clock_runner(self, group):
        db = SessionLocal()
        tags = tag_crud.get_tags_for_group(db, group.id)
        db.close()
        while self.running:
            now = datetime.now()
            minutes = [int(m) for m in group.schedule_details.split(',') if m.strip().isdigit()]
            next_minute = min((m for m in minutes if m > now.minute), default=min(minutes))
            next_run = now.replace(minute=next_minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(hours=1)
            await asyncio.sleep((next_run - now).total_seconds())
            await self._log_tags(group, tags)

    async def _specific_runner(self, group):
        db = SessionLocal()
        tags = tag_crud.get_tags_for_group(db, group.id)
        db.close()
        run_time = datetime.fromisoformat(group.schedule_details)
        now = datetime.now()
        if run_time <= now:
            return
        await asyncio.sleep((run_time - now).total_seconds())
        await self._log_tags(group, tags)

# inside LoggerEngine class
    async def _log_tags(self, group, tags):
        db = SessionLocal()
        client = await get_opc_client(group.server_id)
        if not client:
            logging.warning(f"Group '{group.name}' OPC connection failed.")
            return
        timestamp = datetime.now()
        records = []
        influx_points = []

        for tag in tags:
            try:
                node = client.get_node(tag.node_id)
                data = await node.read_data_value()
                value = str(data.Value.Value) if data.StatusCode.is_good() else None

                records.append({
                    "tag_id": tag.id,
                    "timestamp": timestamp,
                    "value": value,
                    "status_code": data.StatusCode.name
                })

                influx_points.append({
                    "measurement": "opc_tag_data",
                    "tags": {
                        "group": group.name,
                        "alias": tag.alias,
                        "node_id": tag.node_id
                    },
                    "fields": {
                        "value": float(data.Value.Value) if data.StatusCode.is_good() else 0.0
                    },
                    "time": timestamp.isoformat()
                })

            except Exception as e:
                logging.error(f"Error reading tag {tag.node_id}: {e}")

        log_crud.log_data(db, records)
        db.close()

        if influx_points:
            await log_data_to_influx(influx_points)
