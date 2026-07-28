from db.database_async import student_collection, api_key_collection
from tests.conftest import AsyncFakeCursor


def test_get_student_success(client, monkeypatch, fake_student, fake_key):

    async def mock_find_one(*args, **kwargs):
        return fake_key

    async def mock_find_one_and_update(*args, **kwargs):
        return fake_key

    async def mock_count_documents(*args, **kwargs):
        return 1

    monkeypatch.setattr(api_key_collection, "find_one", mock_find_one)
    monkeypatch.setattr(
        api_key_collection, "find_one_and_update", mock_find_one_and_update
    )

    monkeypatch.setattr(student_collection, "count_documents", mock_count_documents)
    monkeypatch.setattr(
        student_collection,
        "find",
        lambda *args, **kwargs: AsyncFakeCursor([fake_student]),
    )

    res = client.get(
        "/v2/students", headers={"x-api-key": "test-key"}, params={"name": "Arisu"}
    )

    assert res.status_code == 200

    data = res.json()

    assert data["students"][0]["name"] == "Arisu"
    assert data["total"] == 1


def test_get_all_student_success(client, monkeypatch, fake_students_list, fake_key):

    async def mock_find_one(*args, **kwargs):
        return fake_key

    async def mock_find_one_and_update(*args, **kwargs):
        return fake_key

    async def mock_count_documents(*args, **kwargs):
        return 1

    monkeypatch.setattr(api_key_collection, "find_one", mock_find_one)
    monkeypatch.setattr(
        api_key_collection, "find_one_and_update", mock_find_one_and_update
    )

    monkeypatch.setattr(student_collection, "count_documents", mock_count_documents)
    monkeypatch.setattr(
        student_collection,
        "find",
        lambda *args, **kwargs: AsyncFakeCursor(fake_students_list),
    )

    res = client.get(
        "/v2/students", headers={"x-api-key": "test-key"}, params={"base_name": "Arisu"}
    )

    assert res.status_code == 200

    data = res.json()

    assert data["students"][0]["name"] == "Arisu"
    assert data["total"] == 1


# Activation: python -m pytest tests/v2/test_student.py
