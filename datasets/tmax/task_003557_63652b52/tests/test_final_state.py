# test_final_state.py

import os
import re
import requests
import pytest

def test_pipeline_log_format():
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"Log file missing at {log_path}"
    with open(log_path, 'r') as f:
        content = f.read()

    match = re.search(r'\[INFO\] Removed \d+ duplicate records\.', content)
    assert match, "Log file does not contain the expected duplicate removal message format: '[INFO] Removed X duplicate records.'"

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/api/records?account_id=ACC-99281"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized when missing auth token, got {response.status_code}"

def test_api_authorized_and_data():
    url = "http://127.0.0.1:8080/api/records?account_id=ACC-99281"
    headers = {"Authorization": "Bearer secret-agent-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    json_str = response.text.lower()

    assert "jonathan harker" in json_str, "Response JSON does not contain the extracted Customer Name 'Jonathan Harker'."
    assert "acc-99281" in json_str, "Response JSON does not contain the extracted Account ID 'ACC-99281'."
    assert "vampire bats in the server room" in json_str, "Response JSON does not contain the extracted Reported Issue 'vampire bats in the server room'."