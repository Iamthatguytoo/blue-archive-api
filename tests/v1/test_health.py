from pymongo.errors import PyMongoError

def test_health(client, monkeypatch):
    class MockAdminSuccess:
        def command(self, *args, **kwargs):
            return {"ok": 1.0}

    monkeypatch.setattr("services.v1.health_check.client.admin", MockAdminSuccess())

    res = client.get("/health")
    assert res.status_code == 200
    
    data = res.json()
    assert data["status"] == "healthy"
    assert "connection_checks" in data
    assert data["connection_checks"]["mongodb"] is True
    assert "timestamp" in data
    assert "environment" in data


def test_health_mongodb_failure(client, monkeypatch):
    class MockAdmin:
        def command(self, *args, **kwargs):
            raise PyMongoError("DB down")

    monkeypatch.setattr("services.v1.health_check.client.admin", MockAdmin())

    res = client.get("/health")

    assert res.status_code == 503

    data = res.json()
    assert data["detail"]["status"] == "unhealthy"
    assert data["detail"]["connection_checks"]["mongodb"] is False

#Activation: python -m pytest tests/test_health.py