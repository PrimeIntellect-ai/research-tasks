# test_final_state.py

import os
import requests
import pytest
import time

def test_vendored_engine_bug_fixed():
    recursion_file = "/app/vendored/graph-engine-0.4.2/src/recursion.rs"
    assert os.path.isfile(recursion_file), f"File {recursion_file} is missing."

    with open(recursion_file, "r") as f:
        content = f.read()
        assert "panic!(" not in content, "The panic statement in recursion.rs was not removed."

def test_service_unauthorized():
    url = "http://127.0.0.1:9090/query"
    payload = {"start_node": "root", "max_depth": 5}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not reachable at 127.0.0.1:9090")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_service_authorized_query():
    url = "http://127.0.0.1:9090/query"
    headers = {
        "Authorization": "Bearer sc-analytics-2024"
    }
    payload = {"start_node": "root", "max_depth": 5}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not reachable at 127.0.0.1:9090")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "result" in data, "Response JSON missing 'result' key"
    assert data["result"] == 450, f"Expected result 450, got {data['result']}"