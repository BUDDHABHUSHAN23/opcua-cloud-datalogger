# backend/tests/test_healthcheck.py

from app.main import app
from fastapi.testclient import TestClient# ✅ CORRECT
from tests.utils import transport

client = TestClient(app)

def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]
 