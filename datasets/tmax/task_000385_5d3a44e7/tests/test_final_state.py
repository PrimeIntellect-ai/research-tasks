# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"
ENDPOINT = f"{BASE_URL}/build-config"
AUTH_TOKEN = "Z98-KML-001"
TARGET = "prod-db-primary"

def test_server_running_and_unauthorized():
    """Test that the server is running and rejects invalid tokens."""
    try:
        response = requests.post(
            ENDPOINT,
            headers={"Authorization": "Bearer wrong-token", "Content-Type": "application/json"},
            json={"service_name": "test"},
            timeout=2
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {ENDPOINT}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for invalid token, got {response.status_code}"

def test_authenticated_standardization_1():
    """Test authenticated request and service name normalization."""
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"service_name": "API_Gateway-v2!"}

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {ENDPOINT}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    expected_yaml = f"""service: apigatewayv2
target: {TARGET}
managed_by: automation_specialist"""

    assert response.text.strip() == expected_yaml, f"Response body did not match expected YAML.\nExpected:\n{expected_yaml}\nGot:\n{response.text.strip()}"

def test_authenticated_standardization_2():
    """Test authenticated request with weird service name."""
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"service_name": "  $$$$__WEIRD___NaMe  "}

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {ENDPOINT}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    expected_yaml = f"""service: weirdname
target: {TARGET}
managed_by: automation_specialist"""

    assert response.text.strip() == expected_yaml, f"Response body did not match expected YAML.\nExpected:\n{expected_yaml}\nGot:\n{response.text.strip()}"