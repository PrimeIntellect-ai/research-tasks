# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer FINOPS_SECRET_99X"}

def test_health_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /health endpoint: {e}")

    assert response.status_code == 200, f"Expected status 200 for /health, got {response.status_code}"
    assert response.text.strip() == "OK", f"Expected body 'OK' for /health, got {response.text}"

def test_cost_endpoint_no_auth():
    try:
        response = requests.get(f"{BASE_URL}/cost?region=eu-central-1", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /cost endpoint: {e}")

    assert response.status_code == 401, f"Expected status 401 for missing auth, got {response.status_code}"

def test_cost_endpoint_wrong_auth():
    try:
        response = requests.get(
            f"{BASE_URL}/cost?region=ap-northeast-1", 
            headers={"Authorization": "Bearer WRONG_TOKEN"},
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /cost endpoint: {e}")

    assert response.status_code == 401, f"Expected status 401 for wrong auth, got {response.status_code}"

@pytest.mark.parametrize("region, expected_cost", [
    ("us-east-1", "0.02"),
    ("eu-central-1", "0.04"),
    ("ap-northeast-1", "0.09"),
    ("sa-east-1", "0.15")
])
def test_cost_endpoint_valid_regions(region, expected_cost):
    try:
        response = requests.get(
            f"{BASE_URL}/cost?region={region}", 
            headers=AUTH_HEADER,
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /cost endpoint: {e}")

    assert response.status_code == 200, f"Expected status 200 for region {region}, got {response.status_code}"
    assert response.text.strip() == expected_cost, f"Expected cost '{expected_cost}' for region {region}, got '{response.text}'"

def test_cost_endpoint_invalid_region():
    try:
        response = requests.get(
            f"{BASE_URL}/cost?region=invalid-region-99", 
            headers=AUTH_HEADER,
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /cost endpoint: {e}")

    assert response.status_code == 404, f"Expected status 404 for invalid region, got {response.status_code}"