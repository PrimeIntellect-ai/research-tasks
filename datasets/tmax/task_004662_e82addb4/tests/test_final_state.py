# test_final_state.py

import os
import requests
import pytest

def test_service_ready_log():
    log_path = "/home/user/service_ready.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. The service might not have started correctly."
    with open(log_path, "r") as f:
        content = f.read()
    assert "SERVICE STARTED" in content, f"Log file {log_path} does not contain 'SERVICE STARTED'."

def test_api_audit_endpoint():
    url = "http://127.0.0.1:8080/api/audit"
    headers = {
        "Authorization": "Bearer COMPLIANCE_AUDIT_77x",
        "Content-Type": "application/json"
    }
    payload = {
        "hr_db": "/data/hr.db",
        "access_logs": "/data/access_logs.json",
        "comm_graph": "/data/comm_graph.csv"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert isinstance(data, list), f"Expected response to be a JSON array, got {type(data).__name__}."

    for item in data:
        assert isinstance(item, str), f"Expected array elements to be strings (employee IDs), got {type(item).__name__}."

    # The default dataset is seeded with exactly two employees meeting the criteria
    assert len(data) == 2, f"Expected exactly 2 flagged employees for the default dataset, but got {len(data)}. IDs returned: {data}"