# test_final_state.py
import os
import requests
import time
import pytest

def test_startup_log():
    log_path = "/home/user/app/startup.log"
    assert os.path.isfile(log_path), f"Startup log missing at {log_path}"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "SERVICES_READY" in content, f"Expected 'SERVICES_READY' in startup.log, found: {content}"

def test_nginx_proxy_and_matrix_pow():
    url = "http://127.0.0.1:9000/api/matrix_pow"
    headers = {"Content-Type": "application/json"}

    test_cases = [
        {
            "payload": {"matrix": [[2, 0], [0, 2]], "n": 3},
            "expected": {"result": [[8, 0], [0, 8]]}
        },
        {
            "payload": {"matrix": [[1, 1], [1, 0]], "n": 0},
            "expected": {"result": [[1, 0], [0, 1]]}
        },
        {
            "payload": {"matrix": [[1, 1], [1, 0]], "n": 5},
            "expected": {"result": [[8, 5], [5, 3]]}
        },
        {
            "payload": {"matrix": [[1, 1], [1, 0]], "n": 10},
            "expected": {"result": [[89, 55], [55, 34]]}
        }
    ]

    for case in test_cases:
        try:
            response = requests.post(url, json=case["payload"], headers=headers, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to Nginx proxy at {url}: {e}")

        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "result" in data, f"Response JSON missing 'result' key: {data}"
        assert data["result"] == case["expected"]["result"], f"For payload {case['payload']}, expected {case['expected']['result']} but got {data['result']}"