from db.database import student_collection
from tests.conftest import FakeCursor


def test_get_student_success(client, mock_api_key, monkeypatch, fake_student):
    monkeypatch.setattr(
        student_collection,
        "find",
        lambda *a, **k: FakeCursor([fake_student])
    )
    monkeypatch.setattr(student_collection, "count_documents", lambda q: 1)

    res = client.get(
        "/students",
        headers={"x-api-key": "test-key"},
        params={"name": "Arisu"}
    )

    assert res.status_code == 200

    data = res.json()
    assert data["students"][0]["name"] == "Arisu"
    assert data["total"] == 1


def test_get_all_student_success(client, mock_api_key, monkeypatch, fake_students_list):
    monkeypatch.setattr(
        student_collection,
        "services.retrieve_students.student_collection.find",
        lambda *a, **k: FakeCursor(fake_students_list)
    )
    monkeypatch.setattr(student_collection, "services.retrieve_students.student_collection.count_documents", lambda q: 0)

    res = client.get(
        "/students",
        headers={"x-api-key": "test-key"},
        params={"base_name": "Arisu"}
    )

    assert res.status_code == 200

    data = res.json()
    assert len(data["students"]) == 3
    assert all(s["base_name"] == "Arisu" for s in data["students"])

#Activation: python -m pytest tests/test_student.py