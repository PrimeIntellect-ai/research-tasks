# test_final_state.py

import os
import json
import time
import socket
import urllib.request
import concurrent.futures
import numpy as np
import pytest

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def test_services_running():
    assert is_port_open(6379), "Redis is not running on port 6379"
    assert is_port_open(8001), "Rust Math Engine is not running on port 8001"
    assert is_port_open(8000), "Python FastAPI Gateway is not running on port 8000"

def test_build_and_start_script_exists():
    path = "/home/user/app/build_and_start.sh"
    assert os.path.isfile(path), f"Script {path} does not exist"
    assert os.access(path, os.X_OK), f"Script {path} is not executable"

def test_functional_correctness():
    url = "http://localhost:8000/api/v1/matrix/determinant"
    data = json.dumps({"matrix": [[1, 2], [3, 4]]}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res = json.loads(response.read().decode())
            assert "determinant" in res, "Response missing 'determinant' key"
            assert abs(res["determinant"] - (-2.0)) < 1e-5, f"Expected determinant -2.0, got {res['determinant']}"
    except Exception as e:
        pytest.fail(f"Functional test failed to communicate with gateway: {e}")

def test_latency_metric():
    url = "http://localhost:8000/api/v1/matrix/determinant"
    data = json.dumps({"matrix": [[2, 0], [0, 2]]}).encode('utf-8')

    latencies = []

    def fetch():
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        start = time.time()
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                response.read()
        except Exception:
            pass
        return (time.time() - start) * 1000

    # Fire 1000 requests using threads to simulate concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(fetch) for _ in range(1000)]
        for f in concurrent.futures.as_completed(futures):
            latencies.append(f.result())

    assert len(latencies) == 1000, "Did not complete 1000 requests"

    p95_latency = np.percentile(latencies, 95)
    assert p95_latency <= 25.0, f"p95 latency is {p95_latency:.2f} ms, which exceeds the 25.0 ms threshold."