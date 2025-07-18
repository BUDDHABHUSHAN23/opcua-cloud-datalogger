# Test Groups API
# tests/test_groups.py

import pytest
from httpx import AsyncClient
from app.main import app
from app.db.database import get_db
from app.db.models.server import Server
from app.db.models.group import Group
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

@pytest.mark.asyncio
async def test_create_group():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First create a server to associate with
        server_payload = {"name": "GroupTestServer", "endpoint_url": "opc.tcp://localhost:4840"}
        server_resp = await ac.post("/api/servers/", json=server_payload)
        assert server_resp.status_code == 201
        server_id = server_resp.json()["id"]

        # Now create a group
        group_payload = {"name": "TestGroup", "server_id": server_id}
        group_resp = await ac.post("/api/groups/", json=group_payload)
        assert group_resp.status_code == 201
        assert group_resp.json()["name"] == "TestGroup"

@pytest.mark.asyncio
async def test_get_groups():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/groups/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
