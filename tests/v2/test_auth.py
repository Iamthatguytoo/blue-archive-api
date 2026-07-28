from db.database_async import api_key_collection, student_collection
from tests.conftest import AsyncFakeCursor
from datetime import datetime, timezone
import pytest
from auth.v2.key_verification import verify_key
from fastapi import HTTPException


def test_missing_api_key(client):
    res = client.get("/v2/students")

    assert res.status_code == 403
    assert res.json()["detail"] == "API key required"


@pytest.mark.anyio
async def test_invalid_api_key(monkeypatch):
    async def mock_find_one(*args, **kwargs):
        return None

    monkeypatch.setattr(api_key_collection, "find_one", mock_find_one)

    with pytest.raises(HTTPException) as exc_info:
        await verify_key(api_key="wrong_key")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Invalid API key"


def test_valid_api_key(client, monkeypatch, fake_students_list):
    fake_key = {
        "_id": "123",
        "api_key": "test-key",
        "requests_today": 0,
        "daily_limit": 10,
        "resetted_at": datetime.now(timezone.utc).date().isoformat(),
        "tier": "free",
    }

    async def mock_fake_key(*args, **kwargs):
        return fake_key

    async def mock_update_one(*args, **kwargs):
        return None

    async def mock_count_documents(*args, **kwargs):
        return 1

    monkeypatch.setattr(api_key_collection, "find_one", mock_fake_key)
    monkeypatch.setattr(api_key_collection, "update_one", mock_update_one)
    monkeypatch.setattr(api_key_collection, "find_one_and_update", mock_fake_key)

    monkeypatch.setattr(student_collection, "count_documents", mock_count_documents)

    monkeypatch.setattr(
        student_collection,
        "find",
        lambda *args, **kwargs: AsyncFakeCursor(fake_students_list),
    )

    res = client.get("/v2/students", headers={"x-api-key": "test-key"})

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
        "tier": "free",
    }

    async def mock_fake_key(*args, **kwargs):
        return fake_key

    async def mock_update_one(*args, **kwargs):
        return None

    monkeypatch.setattr(api_key_collection, "find_one", mock_fake_key)
    monkeypatch.setattr(api_key_collection, "find_one_and_update", mock_update_one)

    res = client.get("/v2/students", headers={"x-api-key": "test-key"})

    assert res.status_code == 429
    assert "Daily limit exceeded" in res.json()["detail"]
