# test_final_state.py
import requests
import pytest

API_URL = "http://127.0.0.1:8000/api/v1/query"
HEADERS = {"Authorization": "Bearer build-ops-xyz-99"}

def test_api_unauthorized():
    """Verify that requests without the correct token return 401 Unauthorized."""
    response = requests.post(API_URL, json={"expression_index": 0})
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_api_valid_expression_0():
    """Verify that expression 0 is correctly extracted and evaluated."""
    response = requests.post(API_URL, json={"expression_index": 0}, headers=HEADERS)
    if response.status_code == 429:
        pytest.skip("Rate limited early, cannot test expression 0 reliably without waiting.")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data.get("index") == 0, f"Expected index 0, got {data.get('index')}"
    assert data.get("result") == 6, f"Expected result 6 for expression 0, got {data.get('result')}"

def test_api_valid_expression_1():
    """Verify that expression 1 is correctly extracted and evaluated."""
    response = requests.post(API_URL, json={"expression_index": 1}, headers=HEADERS)
    if response.status_code == 429:
        pytest.skip("Rate limited early, cannot test expression 1 reliably without waiting.")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data.get("index") == 1, f"Expected index 1, got {data.get('index')}"
    assert data.get("result") == 3, f"Expected result 3 for expression 1, got {data.get('result')}"

def test_api_rate_limiting():
    """Verify that rate limiting (max 3 requests per minute) is enforced."""
    # We will make up to 4 additional requests to ensure we hit the rate limit.
    # Since previous tests may have consumed some quota, we stop as soon as we see a 429.
    hit_429 = False
    for _ in range(4):
        response = requests.post(API_URL, json={"expression_index": 0}, headers=HEADERS)
        if response.status_code == 429:
            hit_429 = True
            break

    assert hit_429, "Rate limiting failed: did not receive 429 Too Many Requests after exceeding quota."