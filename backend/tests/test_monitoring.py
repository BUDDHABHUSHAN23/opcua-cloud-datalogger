# Test Monitoring API
# tests/test_monitoring.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app, raise_app_exceptions=True)

@pytest.mark.asyncio
async def test_start_monitoring():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Start monitoring for a specific server
        payload = {"server_id": 1}
        response = await ac.post("/api/monitor/start", json=payload)
        assert response.status_code in [200, 400]  # Accept if already started
