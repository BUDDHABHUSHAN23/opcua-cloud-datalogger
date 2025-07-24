# app/services/influx_writer.py

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import logging
from datetime import datetime

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env values
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

# Initialize InfluxDB client
client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)
write_api = client.write_api(write_options=SYNCHRONOUS)

def log_data_to_influx(records: list[Point]):
    if not records:
        return

    try:
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=records)
        logger.info(f"Wrote {len(records)} points to InfluxDB.")
    except Exception as e:
        logger.error(f"InfluxDB write failed: {e}")

def create_point(server_name, tag_name, value, timestamp=None):
    time = timestamp or datetime.utcnow()

    return (
        Point("opc_tags")
        .tag("group", server_name)
        .tag("alias", tag_name)
        .tag("node_id", tag_name)
        .field("value", float(value))
        .time(time, WritePrecision.NS)
    )

def write_tag_value(server_name, tag_name, value, timestamp=None):
    point = create_point(server_name, tag_name, value, timestamp)
    log_data_to_influx([point])
