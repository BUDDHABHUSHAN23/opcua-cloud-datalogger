import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_save_tags_without_group(test_db):
    test_tags = [
        {
            "server_id": 1,
            "node_id": "ns=2;s=Test1",
            "alias": "TestTag1",
            "data_type": "Float",
            "sampling_rate": 5
        },
        {
            "server_id": 1,
            "node_id": "ns=2;s=Test2",
            "alias": "TestTag2",
            "data_type": "Boolean",
            "sampling_rate": 5
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/tags/", json=test_tags)

    assert response.status_code in [200, 201]
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_save_tags_to_group(test_db):
    test_tags = [
        {
            "server_id": 1,
            "node_id": "ns=2;s=TestGrouped1",
            "alias": "GroupTag1",
            "data_type": "Float",
            "sampling_rate": 5
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/tags/1", json=test_tags)

    assert response.status_code in [200, 201]
    assert "detail" in response.json()
