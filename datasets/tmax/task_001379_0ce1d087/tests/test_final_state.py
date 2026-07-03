# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import pytest

EXPECTED_WEIGHTS = {
    "utils": 10.0,
    "db": 25.0,
    "auth": 27.5,
    "api": 48.75
}

def test_migration_order_json():
    filepath = "/home/user/workspace/migration_order.json"
    assert os.path.isfile(filepath), f"File {filepath} is missing. The analyzer script must serialize results to this file."

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} does not contain valid JSON.")

    assert data == EXPECTED_WEIGHTS, f"The computed weights in {filepath} do not match the expected values. Got: {data}, Expected: {EXPECTED_WEIGHTS}"

def test_nginx_proxy_routing():
    url = "http://127.0.0.1:8080/api/weights"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 from proxy, got {response.status}"
            content_type = response.headers.get('Content-Type', '')
            assert 'application/json' in content_type, f"Expected application/json content type, got {content_type}"

            body = response.read().decode('utf-8')
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                pytest.fail("Proxy response is not valid JSON.")

            assert data == EXPECTED_WEIGHTS, f"Proxy response data does not match expected weights. Got: {data}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy at {url}. Is Nginx running and configured properly? Error: {e}")

def test_pytest_log_exists_and_passed():
    log_path = "/home/user/workspace/test_results.log"
    assert os.path.isfile(log_path), f"Test log file {log_path} is missing."

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()

    assert "passed" in content, f"The test log at {log_path} does not indicate passing tests. Ensure 'pytest' was run and logged."

def test_analyzer_script_exists():
    assert os.path.isfile("/home/user/workspace/analyzer.py"), "The script /home/user/workspace/analyzer.py is missing."

def test_test_analyzer_script_exists():
    assert os.path.isfile("/home/user/workspace/test_analyzer.py"), "The unit test file /home/user/workspace/test_analyzer.py is missing."