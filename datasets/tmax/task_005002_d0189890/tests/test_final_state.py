# test_final_state.py

import os
import socket
import json
import requests
import concurrent.futures
import pytest

BASE_DIR = "/app/vendored/py-sync-server-1.0.0"

def expected_convergence(data, threshold):
    val = float(sum(data))
    while val >= threshold:
        delta = val * 0.1
        val -= delta
    return val

def test_compute_utils_py_exists():
    """Check that compute_utils.py has been recovered."""
    py_path = os.path.join(BASE_DIR, "compute_utils.py")
    assert os.path.isfile(py_path), f"File {py_path} was not recovered."

def test_http_endpoint():
    """Test the HTTP endpoint for correct response and auth."""
    url = "http://127.0.0.1:8080/sync"
    headers = {"Authorization": "Bearer secret-token-123"}
    payload = {"data": [10, 20, 30], "threshold": 5}

    # Test without auth
    resp_no_auth = requests.post(url, json=payload)
    assert resp_no_auth.status_code in (401, 403), "HTTP endpoint should reject requests without valid auth."

    # Test with auth
    resp = requests.post(url, headers=headers, json=payload)
    assert resp.status_code == 200, f"HTTP endpoint failed with status {resp.status_code}: {resp.text}"

    data = resp.json()
    assert "result" in data, "Response JSON missing 'result' key."

    expected = expected_convergence([10, 20, 30], 5)
    result = float(data["result"])
    assert abs(result - expected) < 1.0, f"Expected converged value around {expected}, got {result}"

def test_tcp_endpoint():
    """Test the TCP endpoint for correct response."""
    host = "127.0.0.1"
    port = 8081

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((host, port))
        s.sendall(b"10,20,30|5\n")
        response = s.recv(1024).decode('utf-8').strip()
    finally:
        s.close()

    assert response, "No response received from TCP endpoint."

    expected = expected_convergence([10, 20, 30], 5)
    result = float(response)
    assert abs(result - expected) < 1.0, f"Expected converged value around {expected}, got {result}"

def make_http_request():
    url = "http://127.0.0.1:8080/sync"
    headers = {"Authorization": "Bearer secret-token-123"}
    payload = {"data": [10, 20, 30], "threshold": 5}
    resp = requests.post(url, headers=headers, json=payload, timeout=5)
    return resp.status_code == 200

def make_tcp_request():
    host = "127.0.0.1"
    port = 8081
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((host, port))
        s.sendall(b"10,20,30|5\n")
        response = s.recv(1024).decode('utf-8').strip()
        return bool(response)
    except Exception:
        return False
    finally:
        s.close()

def test_concurrency_no_deadlock():
    """Test both endpoints concurrently to ensure deadlocks are fixed."""
    num_requests = 50
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for _ in range(num_requests // 2):
            futures.append(executor.submit(make_http_request))
            futures.append(executor.submit(make_tcp_request))

        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                pytest.fail(f"Concurrent request failed with exception: {e}")

    assert all(results), "Some concurrent requests failed, indicating a potential deadlock or server crash."