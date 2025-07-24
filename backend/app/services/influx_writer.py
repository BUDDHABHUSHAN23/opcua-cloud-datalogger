# app/services/influx_writer.py

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import logging

# Load from .env or set defaults
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "admin123")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "opcloggerdb")

client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)
write_api = client.write_api(write_options=SYNCHRONOUS)

async def log_data_to_influx(records: list):
    if not records:
        return

    try:
        points = []
        for record in records:
            p = (
                Point(record["measurement"])
                .tag("group", record["tags"]["group"])
                .tag("alias", record["tags"]["alias"])
                .tag("node_id", record["tags"]["node_id"])
                .field("value", record["fields"]["value"])
                .time(record["time"], WritePrecision.NS)
            )
            points.append(p)

        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)
        logging.info(f"✅ Wrote {len(points)} points to InfluxDB.")
    except Exception as e:
        logging.error(f"❌ Failed to write to InfluxDB: {e}")
