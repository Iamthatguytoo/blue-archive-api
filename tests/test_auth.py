from db.database import api_key_collection, student_collection
from tests.conftest import FakeCursor
from datetime import datetime, timezone
import pytest
from auth.key_verification import verify_key
from fastapi import HTTPException

def test_missing_api_key(client):
    res = client.get("/v1/students")

    assert res.status_code == 403
    assert res.json()["detail"] == "API key required"

def test_invalid_api_key(monkeypatch):
    monkeypatch.setattr(api_key_collection, "find_one", lambda *a, **k: None)

    with pytest.raises(HTTPException) as exc_info:
        verify_key(api_key="wrong_key")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Invalid API key"

def test_valid_api_key(client, monkeypatch, fake_students_list):
    fake_key = {
        "_id": "123",
        "api_key": "test-key",
        "requests_today": 0,
        "daily_limit": 10,
        "resetted_at": datetime.now(timezone.utc).date().isoformat(),
        "tier": "free"
    }

    monkeypatch.setattr(api_key_collection, "find_one", lambda *args, **kwargs: fake_key)
    monkeypatch.setattr(api_key_collection, "update_one", lambda *args, **kwargs: None)
    monkeypatch.setattr(api_key_collection, "find_one_and_update", lambda *args, **kwargs: fake_key)

    monkeypatch.setattr(student_collection, "count_documents", lambda *args, **kwargs: 1)
     
    monkeypatch.setattr(student_collection, "find", lambda *args, **kwargs: FakeCursor(fake_students_list))
  
    res = client.get(
        "/v1/students",
        headers={"x-api-key": "test-key"}
    )

    assert res.status_code == 200
    assert res.json()["total"] == 1
    assert res.json()["students"][0]["name"] == "Arisu"

    
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
        "/v1/students",
        headers={"x-api-key": "test-key"}
    )

    assert res.status_code == 429
    assert "Daily limit exceeded" in res.json()["detail"]

#Activation: python -m pytest tests/test_auth.py