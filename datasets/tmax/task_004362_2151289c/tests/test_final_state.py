# test_final_state.py

import os
import re
import json
import requests
import concurrent.futures
import pytest

def test_start_script_exists():
    script_path = "/home/user/start_services.sh"
    assert os.path.isfile(script_path), f"Startup script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Startup script at {script_path} is not executable"

def test_nginx_config_fixed():
    conf_path = "/app/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config missing at {conf_path}"
    with open(conf_path, 'r') as f:
        content = f.read()

    assert "127.0.0.1:3000" in content, "Nginx config was not updated to proxy to the Rust API on port 3000"
    assert "127.0.0.1:9999" not in content, "Nginx config still contains the broken port 9999"

def test_mre_exists():
    mre_path = "/app/rust_api/tests/regression_test.rs"
    assert os.path.isfile(mre_path), f"MRE test file missing at {mre_path}"
    with open(mre_path, 'r') as f:
        content = f.read()
    assert "A7x9F22PqL4mN8vC1bY5zR3wK0jH6tDq" in content, "MRE does not contain the extracted diagnostic payload"

def test_api_processes_payload_concurrently():
    url = "http://127.0.0.1:8080/process"
    bad_payload = {"payload": "A7x9F22PqL4mN8vC1bY5zR3wK0jH6tDq"}
    good_payload = {"payload": "NormalPayload123"}

    def send_request(payload):
        try:
            response = requests.post(url, json=payload, timeout=3)
            return response
        except requests.exceptions.RequestException as e:
            return e

    # Send multiple requests concurrently to ensure no deadlock occurs
    payloads = [bad_payload, good_payload, bad_payload, good_payload]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(send_request, p) for p in payloads]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    for res in results:
        if isinstance(res, Exception):
            pytest.fail(f"Request failed, possibly due to deadlock or service not running: {res}")

        assert res.status_code == 200, f"Expected status code 200, got {res.status_code}. Response: {res.text}"

        try:
            data = res.json()
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON response: {res.text}")

        assert data.get("status") == "processed", f"Expected status 'processed', got {data.get('status')}"