from db.database import api_key_collection
from datetime import datetime, timezone

def test_missing_api_key(client):
    res = client.get("/students")

    assert res.status_code == 403
    assert res.json()["detail"] == "API key required"

def test_invalid_api_key(client):
    res = client.get(
        "/students",
        headers={"x-api-key": "wrong_key"}
    )

    assert res.status_code == 403
    assert res.json()["detail"] == "Invalid API key"

def test_valid_api_key(client, monkeypatch):
    fake_key = {
        "_id": "123",
        "api_key": "test-key",
        "requests_today": 0,
        "daily_limit": 10,
        "resetted_at": datetime.now(timezone.utc).date().isoformat(),
        "tier": "free"
    }

    monkeypatch.setattr(
        api_key_collection,
        "find_one",
        lambda *args, **kwargs: fake_key
    )

    monkeypatch.setattr(
        api_key_collection,
        "find_one_and_update",
        lambda *args, **kwargs: fake_key
    )

    res = client.get(
        "/students",
        headers={"x-api-key": "test-key"}
    )
    assert res.status_code == 200

    
def test_rate_limit_exceeded(client, monkeypatch):
    fake_key = {
        "_id": "123",
        "api_key": "test-key",
        "requests_today": 1000,
        "daily_limit": 1000,
        "resetted_at": datetime.now(timezone.utc).date().isoformat(),
        "tier": "free"
    }

    monkeypatch.setattr(api_key_collection, "find_one", lambda *a, **k: fake_key)
    monkeypatch.setattr(api_key_collection, "find_one_and_update", lambda *a, **k: None)

    res = client.get(
        "/students",
        headers={"x-api-key": "test-key"}
    )

    assert res.status_code == 429
    assert "Daily limit exceeded" in res.json()["detail"]

#Activation: python -m pytest tests/test_auth.py