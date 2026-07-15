import pytest

@pytest.mark.parametrize(
    "payload, expected_status", 
    [
    ({"probability": 0.8, "rate_up": 0.007}, 200),
    ({"rate_up": 0.007}, 422),
    ({"probability": 2, "rate_up": 0.007}, 422),
    ({"probability": 0.8, "rate_up": 2}, 422),
    ],
)
def test_post_analyze(client, mock_api_key, payload, expected_status):
    res = client.post(
        "/v1/analyze-pulls",
        headers={"x-api-key": "test-key"},
        json=payload
    )

    assert res.status_code == expected_status
    data = res.json()
    if expected_status == 200:
        assert "required_pulls" in data
        assert "pyroxene_needed" in data
        assert "confidence" in data

    elif expected_status in (400, 422):
        assert "details" or "detail" in data

#Activation: python -m pytest tests/test_analyze.py 