from tests.conftest import AsyncFakeCursor
from db.database_async import api_key_collection, banner_collection

def test_get_banner_success(client, monkeypatch, fake_key):
    async def mock_find_one(*args, **kwargs):
        return fake_key

    async def mock_find_one_and_update(*args, **kwargs):
        return fake_key

    def mock_find(*args, **kwargs):
        return AsyncFakeCursor([])

    monkeypatch.setattr(api_key_collection, "find_one", mock_find_one)
    monkeypatch.setattr(
        api_key_collection,
        "find_one_and_update",
        mock_find_one_and_update,
    )
    monkeypatch.setattr(banner_collection, "find", mock_find)

    res = client.get(
        "/v2/banners",
        headers={"x-api-key": "test-key"},
    )

    assert res.status_code == 200