# test_final_state.py

import os
import requests
import pytest
import time

API_URL = "http://127.0.0.1:8080/api/v1/prepare"
AUTH_HEADER = {"Authorization": "Bearer train-token-99"}

def wait_for_server():
    """Wait for the Go server to be up and running."""
    for _ in range(30):
        try:
            # Just check if the port is open and accepting connections
            response = requests.options(API_URL, timeout=1)
            return True
        except requests.exceptions.RequestException:
            try:
                # Fallback to GET just to see if it responds
                requests.get(API_URL, timeout=1)
                return True
            except requests.exceptions.RequestException:
                time.sleep(0.5)
    return False

@pytest.fixture(scope="session", autouse=True)
def ensure_server_running():
    assert wait_for_server(), "The Go HTTP server is not listening on 127.0.0.1:8080"

def test_tables_go_generated():
    """Check that tables.go was successfully generated in the vendored library."""
    assert os.path.isfile("/app/vendored/statslib/tables.go"), "tables.go was not generated in /app/vendored/statslib"

def test_go_mod_exists_and_replaces():
    """Check that the go.mod file exists and contains the correct replace directive."""
    go_mod_path = "/home/user/ml-api/go.mod"
    assert os.path.isfile(go_mod_path), f"{go_mod_path} does not exist"
    with open(go_mod_path, "r") as f:
        content = f.read()
    assert "replace github.com/local/statslib => /app/vendored/statslib" in content or \
           "replace github.com/local/statslib => /app/vendored/statslib" in content.replace("\t", " "), \
           "go.mod does not contain the correct replace directive for github.com/local/statslib"

def test_main_go_exists():
    """Check that main.go exists."""
    assert os.path.isfile("/home/user/ml-api/main.go"), "/home/user/ml-api/main.go does not exist"

def test_api_invalid_auth():
    """Test that the API rejects requests with invalid or missing authentication."""
    # Missing auth
    response = requests.post(API_URL, json={"data": []})
    assert response.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {response.status_code}"

    # Invalid auth
    response = requests.post(API_URL, headers={"Authorization": "Bearer wrong-token"}, json={"data": []})
    assert response.status_code in (401, 403), f"Expected 401 or 403 for invalid auth, got {response.status_code}"

def test_api_invalid_schema():
    """Test that the API rejects data with an invalid schema."""
    # Missing feature_1
    payload = {"data": [{"feature_2": 2.0, "target": 10.5}]}
    response = requests.post(API_URL, headers=AUTH_HEADER, json=payload)
    assert response.status_code == 400, f"Expected 400 for missing feature_1, got {response.status_code}"
    assert response.json().get("error") == "invalid schema", "Expected error message 'invalid schema'"

    # Extra key
    payload = {"data": [{"feature_1": 1.0, "feature_2": 2.0, "target": 10.5, "extra": 1.0}]}
    response = requests.post(API_URL, headers=AUTH_HEADER, json=payload)
    assert response.status_code == 400, f"Expected 400 for extra key, got {response.status_code}"
    assert response.json().get("error") == "invalid schema", "Expected error message 'invalid schema'"

    # Non-numeric value
    payload = {"data": [{"feature_1": "string", "feature_2": 2.0, "target": 10.5}]}
    response = requests.post(API_URL, headers=AUTH_HEADER, json=payload)
    assert response.status_code == 400, f"Expected 400 for non-numeric value, got {response.status_code}"
    assert response.json().get("error") == "invalid schema", "Expected error message 'invalid schema'"

def test_api_valid_schema_regression_ready():
    """Test that the API correctly processes valid data and returns the correct response."""
    payload = {
        "data": [
            {"feature_1": 10.0, "feature_2": 5.0, "target": 2.0},
            {"feature_1": 12.0, "feature_2": 5.0, "target": 2.0}
        ]
    }
    response = requests.post(API_URL, headers=AUTH_HEADER, json=payload)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data.get("schema_valid") is True, "Expected schema_valid to be true"

    # Calculate expected CI bounds based on the dummy implementation
    # mean = (10.0 + 12.0) / 2 = 11.0
    # lower = 11.0 - 1.96 = 9.04
    # upper = 11.0 + 1.96 = 12.96
    expected_lower = 9.04
    expected_upper = 12.96

    assert abs(data.get("ci_lower", 0) - expected_lower) < 1e-5, f"Expected ci_lower ~ {expected_lower}, got {data.get('ci_lower')}"
    assert abs(data.get("ci_upper", 0) - expected_upper) < 1e-5, f"Expected ci_upper ~ {expected_upper}, got {data.get('ci_upper')}"

    # 9.04 > 0.0 and 12.96 < 100.0, so regression_ready should be true
    assert data.get("regression_ready") is True, "Expected regression_ready to be true based on CI bounds"

def test_api_valid_schema_not_regression_ready():
    """Test that the API correctly identifies data not ready for regression."""
    payload = {
        "data": [
            {"feature_1": -5.0, "feature_2": 5.0, "target": 2.0},
            {"feature_1": -3.0, "feature_2": 5.0, "target": 2.0}
        ]
    }
    response = requests.post(API_URL, headers=AUTH_HEADER, json=payload)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data.get("schema_valid") is True, "Expected schema_valid to be true"

    # Calculate expected CI bounds based on the dummy implementation
    # mean = (-5.0 + -3.0) / 2 = -4.0
    # lower = -4.0 - 1.96 = -5.96
    # upper = -4.0 + 1.96 = -2.04
    expected_lower = -5.96
    expected_upper = -2.04

    assert abs(data.get("ci_lower", 0) - expected_lower) < 1e-5, f"Expected ci_lower ~ {expected_lower}, got {data.get('ci_lower')}"
    assert abs(data.get("ci_upper", 0) - expected_upper) < 1e-5, f"Expected ci_upper ~ {expected_upper}, got {data.get('ci_upper')}"

    # -5.96 is not > 0.0, so regression_ready should be false
    assert data.get("regression_ready") is False, "Expected regression_ready to be false based on CI bounds"