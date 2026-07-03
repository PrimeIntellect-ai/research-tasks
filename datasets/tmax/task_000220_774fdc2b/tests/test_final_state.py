# test_final_state.py

import os
import json
import time
import pytest
import requests

API_URL = "http://127.0.0.1:8080"
HEADERS = {"Authorization": "Bearer secret_impute_token_99"}

def test_service_ready_log():
    log_path = "/app/service_ready.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. Did you start the service and write 'READY'?"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "READY" in content, f"Expected 'READY' in {log_path}, got: {content}"

def test_api_unauthorized():
    # Test without header
    try:
        resp = requests.get(f"{API_URL}/api/record/1", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {API_URL}: {e}")

    assert resp.status_code in (401, 403), f"Expected 401 or 403 for unauthorized request, got {resp.status_code}"

    # Test with wrong header
    wrong_headers = {"Authorization": "Bearer wrong_token"}
    resp = requests.get(f"{API_URL}/api/record/1", headers=wrong_headers, timeout=2)
    assert resp.status_code in (401, 403), f"Expected 401 or 403 for invalid token, got {resp.status_code}"

def test_api_get_record_success():
    resp = requests.get(f"{API_URL}/api/record/1", headers=HEADERS, timeout=2)
    assert resp.status_code == 200, f"Expected 200 OK for valid record, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "id" in data, "Response JSON missing 'id'"
    assert "tokens" in data, "Response JSON missing 'tokens'"
    assert "readings" in data, "Response JSON missing 'readings'"

    assert data["id"] == 1, f"Expected id=1, got {data['id']}"
    assert isinstance(data["tokens"], list), "'tokens' should be a list"
    assert isinstance(data["readings"], list), "'readings' should be a list"

def test_api_get_record_not_found():
    resp = requests.get(f"{API_URL}/api/record/9999", headers=HEADERS, timeout=2)
    assert resp.status_code == 404, f"Expected 404 for non-existent record, got {resp.status_code}"

def test_api_post_export():
    export_path = "/app/export.csv"
    if os.path.exists(export_path):
        os.remove(export_path)

    resp = requests.post(f"{API_URL}/api/export", headers=HEADERS, timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK for export, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert data.get("status") == "success", f"Expected {{'status': 'success'}}, got {data}"

    # Wait briefly for export file to be written if it's async, though it should be sync
    for _ in range(10):
        if os.path.exists(export_path):
            break
        time.sleep(0.1)

    assert os.path.exists(export_path), f"Export file {export_path} was not created"
    assert os.path.getsize(export_path) > 0, f"Export file {export_path} is empty"