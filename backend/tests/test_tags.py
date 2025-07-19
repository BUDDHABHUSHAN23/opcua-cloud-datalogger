# Test Tags API
# tests/test_tags.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app, raise_app_exceptions=True)

@pytest.mark.asyncio
async def test_create_tag():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        # Create Server
        server_payload = {"name": "TagTestServer", "endpoint_url": "opc.tcp://localhost:4840"}
        server_resp = await ac.post("/api/servers/", json=server_payload)
        server_id = server_resp.json()["id"]

        # Create Group
        group_payload = {"name": "TagGroup", "server_id": server_id}
        group_resp = await ac.post("/api/groups/", json=group_payload)
        group_id = group_resp.json()["id"]

        # Create Tag
        tag_payload = {
            "name": "TemperatureTag1",
            "alias": "Temp1",
            "node_id": "ns=2;s=Temperature",
            "group_id": group_id,
            "data_type": "float",
            "sampling_rate": 5,
            "enabled": True
        }
        tag_resp = await ac.post("/api/tags/", json=tag_payload)
        assert tag_resp.status_code == 201
        assert tag_resp.json()["alias"] == "Temp1"

@pytest.mark.asyncio
async def test_get_tags():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Fetch all tags
        response = await ac.get("/api/tags/")
        assert response.status_code == 200
