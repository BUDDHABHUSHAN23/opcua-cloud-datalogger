# Test Monitoring API
# tests/test_monitoring.py

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_start_monitoring():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"server_id": 1}
        response = await ac.post("/api/monitor/start", json=payload)
        assert response.status_code in [200, 400]  # Accept if already started
