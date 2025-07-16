from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv

load_dotenv()

INFLUX_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUX_ORG = os.getenv("INFLUXDB_ORG")
INFLUX_BUCKET = os.getenv("INFLUXDB_BUCKET", "opclogger")

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_tag_value(tag_name: str, value: float, timestamp, server_id: int):
    point = (
        Point("opc_tag")
        .tag("tag", tag_name)
        .tag("server_id", str(server_id))
        .field("value", value)
        .time(timestamp, WritePrecision.NS)
    )
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
