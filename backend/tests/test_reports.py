# Test Reports API
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_all_reports():
    response = client.get("/api/reports/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_report_schedule():
    payload = {
        "name": "Test Report Schedule",
        "group_id": 1,  # must exist in DB or will fail
        "output_folder": "output/",
        "report_format": "Excel",
        "template_path": "",
        "schedule_type": "On Interval",
        "is_enabled": True
    }
    response = client.post("/api/reports/", json=payload)
    assert response.status_code in (200, 201, 400)  # depends on whether group_id exists
    if response.status_code == 400:
        assert "already exists" in response.text or "invalid" in response.text.lower()


def test_run_report_manually():
    report_id = 1  # You must ensure this ID exists, or mock it in future
    response = client.post(f"/api/reports/run/{report_id}")
    assert response.status_code in (200, 404)
