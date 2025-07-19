import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from uuid import uuid4

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_get_servers():
    async with AsyncClient(transport=transport, base_url="http://test",follow_redirects=True) as ac:
        response = await ac.get("/api/servers/")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_server():
    async with AsyncClient(transport=transport, base_url="http://test",follow_redirects=True) as ac:
        payload = {
            "name": f"Server_{uuid4().hex[:8]}",
            "endpoint_url": "opc.tcp://localhost:4840"
        }
        response = await ac.post("/api/servers/", json=payload)
        assert response.status_code in [200, 201, 409]  # Allow conflict if already exists
