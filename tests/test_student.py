from db.database import student_collection, api_key_collection
from tests.conftest import FakeCursor


def test_get_student_success(client, mock_api_key, monkeypatch, fake_student):
    monkeypatch.setattr(
        student_collection,
        "find",
        lambda *a, **k: FakeCursor([fake_student])
    )
    monkeypatch.setattr(student_collection, "count_documents", lambda q: 1)

    res = client.get(
        "/v1/students",
        headers={"x-api-key": "test-key"},
        params={"name": "Arisu"}
    )

    assert res.status_code == 200

    data = res.json()
    assert data["students"][0]["name"] == "Arisu"
    assert data["total"] == 1


def test_get_all_student_success(client, monkeypatch, fake_students_list, fake_key):
    
    monkeypatch.setattr(api_key_collection, "find_one", lambda *a, **k: fake_key)
    monkeypatch.setattr(api_key_collection, "find_one_and_update", lambda *a, **k: fake_key)
    
    
    monkeypatch.setattr(student_collection, "count_documents", lambda *a, **k: 1)
    monkeypatch.setattr(student_collection, "find", lambda *a, **k: FakeCursor(fake_students_list))

    res = client.get(
        "/v1/students",
        headers={"x-api-key": "test-key"},
        params={"base_name": "Arisu"}
    )
    assert res.status_code == 200

#Activation: python -m pytest tests/test_student.py