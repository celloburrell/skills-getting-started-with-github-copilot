import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original_participants = app_module.activities["Chess Club"]["participants"][:]
    yield
    app_module.activities["Chess Club"]["participants"] = original_participants


client = TestClient(app_module.app)


def test_unregister_participant_removes_email():
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_not_found():
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "ghost@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
