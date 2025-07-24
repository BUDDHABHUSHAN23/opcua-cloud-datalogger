# backend/app/opcua/connector.py

from asyncua import Client, ua
from asyncua.common.node import Node
from typing import List, Optional
import asyncio
from app.db.database import SessionLocal
from app.db.models.server import Server


class OPCUAConnector:
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        self.client = Client(url=endpoint_url)
        self.connected = False

    async def connect(self):
        try:
            await self.client.connect()
            self.connected = True
            print(f"[OPCUA] Connected to {self.endpoint_url}")
        except Exception as e:
            self.connected = False
            print(f"[OPCUA] Connection failed: {e}")
            raise e

    async def disconnect(self):
        if self.connected:
            await self.client.disconnect()
            self.connected = False
            print(f"[OPCUA] Disconnected from {self.endpoint_url}")

    async def read_value(self, node_id: str) -> Optional[ua.DataValue]:
        if not self.connected:
            await self.connect()

        try:
            node = self.client.get_node(node_id)
            value = await node.read_data_value()
            return value
        except Exception as e:
            print(f"[OPCUA] Failed to read {node_id}: {e}")
            return None

    async def read_multiple(self, node_ids: List[str]) -> dict:
        if not self.connected:
            await self.connect()

        results = {}
        for node_id in node_ids:
            try:
                node = self.client.get_node(node_id)
                value = await node.read_data_value()
                results[node_id] = {
                    "value": value.Value.Value,
                    "status": str(value.StatusCode),
                    "timestamp": str(value.SourceTimestamp)
                }
            except Exception as e:
                results[node_id] = {"error": str(e)}
        return results

    async def browse_root(self):
        root = self.client.nodes.root
        objects = await root.get_children()
        result = []
        for node in objects:
            result.append({
                "nodeId": node.nodeid.to_string(),
                "displayName": str(await node.read_display_name()),
                "type": str(await node.read_node_class())
            })
        return result



# ✅ ADD THIS to support Celery imports:
async def get_opcua_client(server_id: int) -> Optional[Client]:
    db = SessionLocal()
    server = db.query(Server).filter(Server.id == server_id).first()
    db.close()

    if not server:
        print(f"[OPCUA] Server ID {server_id} not found in DB.")
        return None

    connector = OPCUAConnector(server.endpoint_url)
    try:
        await connector.connect()
        return connector.client
    except Exception as e:
        print(f"[OPCUA] Failed to connect to {server.endpoint_url}: {e}")
        return None
