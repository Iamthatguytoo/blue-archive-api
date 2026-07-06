import pytest

@pytest.mark.parametrize("payload, expected_status", [
    ({"pyroxene": 22000, "rate_up": 0.007}, 200),
    ({"pyroxene": 22000}, 200),
    ({"pyroxene": 22000, "rate_up": None}, 422),
    ({"pyroxene": 22000, "rate_up": 0}, 422),
    ({"pyroxene": -1, "rate_up": 0.007}, 422),
])
def test_post_calculate(client, mock_api_key, payload, expected_status):
    res = client.post(
        "/gacha-calculate",
        headers={"x-api-key": "test-key"},
        json=payload
    )

    assert res.status_code == expected_status
    data = res.json()
    if expected_status == 200:
    
        assert "pulls" in data
        assert "spark_reachable" in data
        assert "pulls_to_spark" in data

    elif expected_status in (400, 422):
        assert "details" or "detail" in data

#Activation: python -m pytest tests/test_calculate.py