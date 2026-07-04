# test_final_state.py
import os
import re
import pytest
import requests
import sys

def test_files_exist():
    assert os.path.isfile("/home/user/api.py"), "/home/user/api.py is missing."
    assert os.path.isfile("/home/user/bench.py"), "/home/user/bench.py is missing."

    log_file = "/home/user/bench_results.log"
    assert os.path.isfile(log_file), "/home/user/bench_results.log is missing."

    with open(log_file, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split("\n") if line.strip()]
    assert len(lines) > 0, "bench_results.log is empty."

    last_line = lines[-1]
    assert re.match(r"^Benchmark completed: \d+(\.\d+)?s$", last_line), f"Log output does not match expected format: {last_line}"

def test_fast_eval_installed():
    try:
        import fast_eval
    except ImportError:
        pytest.fail("fast_eval is not installed or cannot be imported.")

    try:
        result = fast_eval.compute("ADD", 2, 3)
        assert result == 5, f"fast_eval.compute('ADD', 2, 3) returned {result}, expected 5."
    except Exception as e:
        pytest.fail(f"fast_eval.compute failed: {e}")

def test_rest_api_valid_request():
    url = "http://127.0.0.1:8080/evaluate"
    headers = {"Authorization": "Bearer eval-secret-777"}
    payload = {"expression": "ADD(5, 5) | MUL(10) | SUB(20)"}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response is not valid JSON.")

    assert "result" in data, "Response JSON missing 'result' key."
    assert data["result"] == 80, f"Expected result 80, got {data['result']}."

def test_rest_api_invalid_auth():
    url = "http://127.0.0.1:8080/evaluate"
    headers = {"Authorization": "Bearer wrong-token"}
    payload = {"expression": "ADD(1, 1)"}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}. Response: {resp.text}"

def test_rest_api_missing_auth():
    url = "http://127.0.0.1:8080/evaluate"
    payload = {"expression": "ADD(1, 1)"}

    try:
        resp = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {resp.status_code}. Response: {resp.text}"