# test_final_state.py

import os
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer super-secret-etl-token"}

def test_api_unauthorized_access():
    """Verify that accessing the API without a valid token returns 401."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/hierarchy/5", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("FastAPI application is not running or not listening on 127.0.0.1:8080.")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_api_hierarchy_endpoint():
    """Verify the hierarchy endpoint returns the correct management chain."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/hierarchy/5", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("FastAPI application is not running or not listening on 127.0.0.1:8080.")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "employee_id" in data, "Response missing 'employee_id' key."
    assert "management_chain" in data, "Response missing 'management_chain' key."

    assert data["employee_id"] == 5, f"Expected employee_id 5, got {data['employee_id']}"
    assert data["management_chain"] == [2, 1], f"Expected management_chain [2, 1], got {data['management_chain']}"

def test_api_cross_reference_endpoint():
    """Verify the cross-reference endpoint returns combined data from Postgres and Neo4j."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/cross-reference/2", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("FastAPI application is not running or not listening on 127.0.0.1:8080.")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data.get("employee_id") == 2, f"Expected employee_id 2, got {data.get('employee_id')}"
    assert data.get("department") == "Engineering", f"Expected department 'Engineering', got {data.get('department')}"
    assert data.get("salary") == 120000, f"Expected salary 120000, got {data.get('salary')}"
    assert data.get("direct_reports_count") == 3, f"Expected direct_reports_count 3, got {data.get('direct_reports_count')}"

def test_startup_log_file_exists():
    """Verify that the API startup log file was created."""
    log_path = "/home/user/api_startup.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."