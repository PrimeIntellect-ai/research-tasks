# test_final_state.py

import os
import time
import pytest
import requests

BASE_URL = "http://127.0.0.1:9090"

@pytest.fixture(scope="session", autouse=True)
def wait_for_server():
    """Wait for the HTTP server to become available."""
    for _ in range(20):
        try:
            resp = requests.get(BASE_URL + "/config", timeout=1)
            if resp.status_code in (200, 401, 403, 404):
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    pytest.fail(f"HTTP server did not start on {BASE_URL}")

def test_get_config_initial_state():
    """Test that the initial GET /config returns the correct merged configuration."""
    resp = requests.get(BASE_URL + "/config", timeout=5)
    assert resp.status_code == 200, f"Expected GET /config to return 200 OK, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {resp.text}")

    assert data.get("maintenance_mode") is True, f"Expected maintenance_mode to be true, got {data.get('maintenance_mode')}"
    assert data.get("max_workers") == 42, f"Expected max_workers to be 42, got {data.get('max_workers')}"
    assert data.get("target_region") == "eu-west-1", f"Expected target_region to be 'eu-west-1', got {data.get('target_region')}"
    assert data.get("log_level") == "INFO", f"Expected log_level to be 'INFO', got {data.get('log_level')}"
    assert data.get("retry_count") == 3, f"Expected retry_count to be 3, got {data.get('retry_count')}"

def test_post_config_auth_and_constraints():
    """Test POST /config authentication and constraints."""
    # 1. Missing Auth
    resp_no_auth = requests.post(BASE_URL + "/config", json={"max_workers": 150}, timeout=5)
    assert resp_no_auth.status_code in (401, 403), f"Expected 401 or 403 when no auth provided, got {resp_no_auth.status_code}"

    headers = {"Authorization": "Bearer admin-token-2024"}

    # 2. Invalid max_workers constraint (> 100)
    resp_invalid_workers = requests.post(BASE_URL + "/config", json={"max_workers": 150}, headers=headers, timeout=5)
    assert resp_invalid_workers.status_code == 400, f"Expected 400 Bad Request for max_workers=150, got {resp_invalid_workers.status_code}"

    # 3. Invalid target_region constraint (doesn't start with eu- or us-)
    resp_invalid_region = requests.post(BASE_URL + "/config", json={"target_region": "ap-south-1"}, headers=headers, timeout=5)
    assert resp_invalid_region.status_code == 400, f"Expected 400 Bad Request for target_region='ap-south-1', got {resp_invalid_region.status_code}"

    # 4. Valid update
    resp_valid = requests.post(BASE_URL + "/config", json={"max_workers": 5, "target_region": "us-west-2"}, headers=headers, timeout=5)
    assert resp_valid.status_code == 200, f"Expected 200 OK for valid update, got {resp_valid.status_code}. Response: {resp_valid.text}"

def test_get_sample():
    """Test GET /sample after max_workers has been updated to 5."""
    resp = requests.get(BASE_URL + "/sample", timeout=10)
    assert resp.status_code == 200, f"Expected GET /sample to return 200 OK, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {resp.text}")

    assert isinstance(data, dict), "Expected sample response to be a JSON object"
    assert len(data) > 0, "Expected sample response to contain keys for status codes"

    for status_code, records in data.items():
        assert isinstance(records, list), f"Expected value for status code {status_code} to be a list"
        # Since max_workers was updated to 5 in the previous test, we expect 5 records
        assert len(records) == 5, f"Expected exactly 5 records for status code {status_code}, got {len(records)}"

def test_log_file_check():
    """Test that the audit log contains the required entries."""
    log_file = "/home/user/config_audit.log"
    assert os.path.isfile(log_file), f"Audit log file not found at {log_file}"

    with open(log_file, "r") as f:
        lines = f.readlines()

    config_updated_lines = [line for line in lines if "CONFIG_UPDATED:" in line]
    assert len(config_updated_lines) >= 2, f"Expected at least 2 'CONFIG_UPDATED:' entries in {log_file}, found {len(config_updated_lines)}"