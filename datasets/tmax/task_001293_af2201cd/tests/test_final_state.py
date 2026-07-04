# test_final_state.py
import requests
import pytest

GATEWAY_URL = "http://127.0.0.1:9000/api/audit/deadlocks"
VALID_TOKEN = "audit_sec_9942"
BAD_TOKEN = "bad_token"

def test_unauthorized_request():
    headers = {"Authorization": f"Bearer {BAD_TOKEN}"}
    try:
        response = requests.get(GATEWAY_URL, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the Gateway service at {GATEWAY_URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for bad token, got {response.status_code}"

def test_valid_request_pagination():
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    params = {"page": 2, "limit": 2}
    try:
        response = requests.get(GATEWAY_URL, headers=headers, params=params, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the Gateway service at {GATEWAY_URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid token, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "total_deadlocks" in data, "Missing 'total_deadlocks' in response"
    assert data["total_deadlocks"] == 5, f"Expected 5 total deadlocks, got {data['total_deadlocks']}"

    assert "page" in data, "Missing 'page' in response"
    assert int(data["page"]) == 2, f"Expected page 2, got {data['page']}"

    assert "limit" in data, "Missing 'limit' in response"
    assert int(data["limit"]) == 2, f"Expected limit 2, got {data['limit']}"

    assert "data" in data, "Missing 'data' in response"
    assert isinstance(data["data"], list), "'data' should be a list"

    # We check if the expected cycles are in the returned data.
    # Depending on the exact sorting implementation, the second page of limit 2 
    # should contain these specific deadlocks as per the truth.
    expected_cycle_1 = ["T10", "T11", "T8", "T9"]
    expected_cycle_2 = ["T20", "T21"]

    assert expected_cycle_1 in data["data"], f"Expected cycle {expected_cycle_1} not found in page 2 data: {data['data']}"
    assert expected_cycle_2 in data["data"], f"Expected cycle {expected_cycle_2} not found in page 2 data: {data['data']}"