import pytest
from httpx import AsyncClient
from uuid import uuid4
from .utils import transport

@pytest.mark.asyncio
async def test_create_group():
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        server_payload = {
            "name": f"GroupTestServer_{uuid4().hex[:6]}",
            "endpoint_url": "opc.tcp://localhost:4840"
        }
        server_resp = await ac.post("/api/servers/", json=server_payload)
        assert server_resp.status_code in [200, 201, 409]

        group_payload = {
            "name": f"Group_{uuid4().hex[:6]}",
            "description": "Test Group",
            "schedule_type": "interval",
            "schedule_details": "10",
            "server_id": server_resp.json().get("id", 1)
        }
        response = await ac.post("/api/groups/", json=group_payload)
        assert response.status_code in [200, 201, 409]

@pytest.mark.asyncio
async def test_get_groups():
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        response = await ac.get("/api/groups/")
        assert response.status_code == 200