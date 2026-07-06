from fastapi.testclient import TestClient
from blue_archive_characters_api import server
from db.database import api_key_collection, client
from datetime import datetime, timezone
import pytest

@pytest.fixture(scope='session')
def client():
    return TestClient(server)

class FakeCursor:
    def __init__(self, data):
        self.data = data

    def skip(self, n):
        return self

    def limit(self, n):
        return self

    def __iter__(self):
        return iter(self.data)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __bool__(self):
        return bool(self.data)

@pytest.fixture
def fake_key():
    return {
        "_id": "123",
        "api_key": "test-key",
        "requests_today": 0,
        "daily_limit": 1000,
        "resetted_at": datetime.now(timezone.utc).date().isoformat(),
        "tier": "free"
    }

@pytest.fixture
def mock_api_key(monkeypatch, fake_key):
    monkeypatch.setattr(api_key_collection, "find_one", lambda *a, **k: fake_key)
    monkeypatch.setattr(api_key_collection, "find_one_and_update", lambda *a, **k: fake_key)


@pytest.fixture
def fake_student():
    return {
        "name": "Arisu",
        "base_name": "Arisu",
        "rarity": "3",
        "variant": None,
        "damage_type": None,
        "armor_type": None,
        "class_name": None,
        "school": None,
        "position": None,
        "weapon": None,
        "pool": None,
        "terrain": {
            "urban_terrain": None,
            "outdoor_terrain": None,
            "indoor_terrain": None
        }
    }


@pytest.fixture
def fake_students_list(fake_student):
    return [fake_student]

#Activate ALL: python -m pytest tests/ -v