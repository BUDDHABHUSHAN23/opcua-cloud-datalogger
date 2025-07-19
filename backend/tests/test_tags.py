import pytest
from httpx import AsyncClient
from uuid import uuid4
from .utils import transport

@pytest.mark.asyncio
async def test_create_tag():
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        server_payload = {
            "name": f"TagServer_{uuid4().hex[:6]}",
            "endpoint_url": "opc.tcp://localhost:4840"
        }
        await ac.post("/api/servers/", json=server_payload)

        payload = {
            "name": f"Tag_{uuid4().hex[:6]}",
            "alias": "TagAlias",
            "server_id": 1,
            "node_id": "ns=2;i=2",
            "data_type": "float",
            "mode": "monitor",
            "sampling_rate": 5,
            "enabled": True
        }
        response = await ac.post("/api/tags/", json=payload)
        assert response.status_code in [200, 201, 409]

@pytest.mark.asyncio
async def test_get_tags():
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        response = await ac.get("/api/tags/")
        assert response.status_code == 200