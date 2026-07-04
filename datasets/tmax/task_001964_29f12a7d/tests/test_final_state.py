# test_final_state.py

import os
import json
import requests
import pytest

def test_makefile_fixed():
    """Test that the Makefile uses the correct linker flag."""
    path = "/app/vendored_data_parser/Makefile"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "-ldata_lib_v2" in content, "Makefile does not contain the correct linker flag '-ldata_lib_v2'."
    assert "-lold_data_lib_v1" not in content, "Makefile still contains the old linker flag '-lold_data_lib_v1'."

def test_schema_validator_exists():
    """Test that schema_validator.py exists."""
    path = "/home/user/schema_validator.py"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_test_schema_validator_exists():
    """Test that test_schema_validator.py exists."""
    path = "/home/user/test_schema_validator.py"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_test_results_log_exists():
    """Test that test_results.log exists."""
    path = "/home/user/test_results.log"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_service_pid_exists():
    """Test that service.pid exists and contains an integer."""
    path = "/home/user/service.pid"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content.isdigit(), f"PID file {path} does not contain a valid integer PID."

def test_http_service_no_token():
    """Test POST /validate with no token returns 401."""
    url = "http://127.0.0.1:8080/validate"
    try:
        response = requests.post(url, json={"data": "deadbeef", "schema_version": "2.4.0"}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to service: {e}")
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_http_service_bad_token():
    """Test POST /validate with bad token returns 401."""
    url = "http://127.0.0.1:8080/validate"
    headers = {"Authorization": "Bearer bad-token"}
    try:
        response = requests.post(url, json={"data": "deadbeef", "schema_version": "2.4.0"}, headers=headers, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to service: {e}")
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_http_service_incompatible_version():
    """Test POST /validate with incompatible version returns 400."""
    url = "http://127.0.0.1:8080/validate"
    headers = {"Authorization": "Bearer release-manager-token-992"}
    payload = {"data": "deadbeef", "schema_version": "3.0.0"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to service: {e}")
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"

def test_http_service_success():
    """Test POST /validate with compatible version returns 200 and parsed data."""
    url = "http://127.0.0.1:8080/validate"
    headers = {"Authorization": "Bearer release-manager-token-992"}
    payload = {"data": "deadbeef", "schema_version": "2.4.0"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to service: {e}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("parsed") == "valid_parser_output_deadbeef", f"Expected parsed data 'valid_parser_output_deadbeef', got {data.get('parsed')}"