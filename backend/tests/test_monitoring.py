import pytest
from httpx import AsyncClient
from app.main import app
from httpx import ASGITransport

transport = ASGITransport(app=app)
@pytest.mark.asyncio
async def test_start_monitoring():
   async with AsyncClient(transport=transport, base_url="http://test",follow_redirects=True) as ac:
        response = await ac.post("/monitor/", json={"server_id": 1, "node_ids": ["ns=2;i=2"]})
        assert response.status_code in [200, 400, 404]
