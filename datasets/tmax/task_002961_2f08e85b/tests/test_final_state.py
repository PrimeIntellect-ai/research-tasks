# test_final_state.py
import pytest
import requests
from decimal import Decimal

URL = "http://127.0.0.1:8080/variance"
AUTH_HEADER = {"X-Auth-Token": "super-secret-token-99"}

def test_server_running_and_unauthorized():
    """Test that the server is running and enforces authentication."""
    try:
        response = requests.post(URL, json={"data": ["1.1", "2.2", "3.3"]}, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not running or not reachable at 127.0.0.1:8080.")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}."

def test_precision_calculation():
    """Test that the server uses Decimal for exact precision calculation."""
    payload = {"data": ["1.1", "2.2", "3.3"]}

    try:
        response = requests.post(URL, headers=AUTH_HEADER, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not running or not reachable at 127.0.0.1:8080.")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code} with body {response.text}"

    data = response.json()
    assert "variance" in data, f"Expected 'variance' in response, got {data}"

    # Compute expected variance using Decimal
    dec_data = [Decimal(x) for x in payload["data"]]
    mean = sum(dec_data) / Decimal(len(dec_data))
    expected_var = sum((x - mean) ** Decimal('2') for x in dec_data) / Decimal(len(dec_data))

    actual_var = Decimal(data["variance"])
    assert actual_var == expected_var, f"Precision issue: expected {expected_var}, got {actual_var}"

def test_corrupted_input_handling():
    """Test that the server gracefully handles corrupted input."""
    payload = {"data": ["1.1", "bad_data", "3.3"]}

    try:
        response = requests.post(URL, headers=AUTH_HEADER, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not running or not reachable at 127.0.0.1:8080.")

    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code} with body {response.text}"

    data = response.json()
    assert data.get("error") == "corrupted input", f"Expected error message 'corrupted input', got {data}"