import pytest

@pytest.mark.parametrize("payload, expected_status", [
    ({"simulations": 100,"pyroxene": 22000}, 200),
    ({"simulations": 1000,"pyroxene": 22000}, 200),
    ({"simulations": 1000, "pyroxene": 22000, "rate_up": 0.008}, 200),
    ({"simulations": 100}, 422),
    ({"pyroxene": 22000}, 422),
    ({"simulations": 1001,"pyroxene": 22000}, 400),
    ({"simulations": 100,"pyroxene": 119}, 400),
    ({"simulations": -1,"pyroxene": 22000}, 422),
    ({"simulations": 1000,"pyroxene": -1}, 422),
    ({"simulations": 1000, "pyroxene": 22000, "rate_up": 0}, 422)
])
def test_post_calculate(client, mock_api_key, payload, expected_status):
    res = client.post(
        "/gacha-simulate",
        headers={"x-api-key": "test-key"},
        json=payload
    )

    assert res.status_code == expected_status
    data = res.json()
    if expected_status == 200:
    
        assert "success_rate" in data
        assert "successful_runs" in data
        assert "simulations_conducted" in data

    elif expected_status in (400, 422):
        assert "details" or "detail" in data

#Activation: python -m pytest tests/test_simulate.py