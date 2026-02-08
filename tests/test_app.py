from fastapi.testclient import TestClient
import pytest

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Make a shallow copy of original participants lists to restore after test
    original = {k: v["participants"][:] for k, v in activities.items()}
    yield
    for k, v in activities.items():
        v["participants"] = original.get(k, [])


def test_get_activities():
    client = TestClient(app)
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    client = TestClient(app)
    activity = "Chess Club"
    email = "tester@example.com"

    # Ensure not present
    assert email not in activities[activity]["participants"]

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister
    r2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert r2.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_missing_participant_returns_404():
    client = TestClient(app)
    activity = "Chess Club"
    email = "notfound@example.com"

    r = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert r.status_code == 404
