import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from dotenv import load_dotenv


load_dotenv(".env.test")


transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_get_servers():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/servers/")
        print("GET /api/servers response:", response.text)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_server():
    payload = {
        "name": "Test OPC Server",
        "endpoint_url": "opc.tcp://localhost:4840"
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/servers/", json=payload)
        print("POST /api/servers response:", response.text)
        assert response.status_code == 201
