# test_final_state.py

import os
import time
import json
import urllib.request
import urllib.error
import subprocess
import pytest
import concurrent.futures

def test_shared_library_and_bugfix():
    so_path = "/home/user/legacy/libsolver.so"
    assert os.path.exists(so_path), f"Shared library {so_path} was not compiled or is missing."

    c_path = "/home/user/legacy/solver.c"
    assert os.path.exists(c_path), f"Source file {c_path} is missing."
    with open(c_path, 'r') as f:
        content = f.read()
    assert "int dp[50]" not in content, "The memory safety bug (fixed-size array `int dp[50]`) is still present in solver.c"

@pytest.fixture(scope="module")
def api_server():
    start_sh = "/home/user/api/start.sh"
    assert os.path.exists(start_sh), f"{start_sh} does not exist."

    # Run the script
    subprocess.run(["bash", start_sh], check=True)
    time.sleep(2)

    pid_file = "/home/user/api/server.pid"
    assert os.path.exists(pid_file), f"PID file {pid_file} was not created."

    yield

    # Cleanup: kill the server
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, 9)
    except Exception:
        pass

def post_json(url, data):
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode(), json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return 0, None

def test_api_valid_request(api_server):
    data = {
        "items": [
            {"weight": 10, "value": 60},
            {"weight": 20, "value": 100},
            {"weight": 30, "value": 120}
        ],
        "capacity": 50
    }
    code, resp = post_json("http://127.0.0.1:8080/solve", data)
    assert code == 200, f"Expected status 200 for a valid request, got {code}"
    assert resp is not None and resp.get("max_value") == 220, f"Expected max_value 220, got {resp}"

def test_api_validation(api_server):
    url = "http://127.0.0.1:8080/solve"

    # Capacity > 1000
    data = {"items": [{"weight": 10, "value": 60}], "capacity": 1500}
    code, _ = post_json(url, data)
    assert code == 400, f"Expected 400 Bad Request for capacity > 1000, got {code}"

    # Capacity < 1
    data = {"items": [{"weight": 10, "value": 60}], "capacity": 0}
    code, _ = post_json(url, data)
    assert code == 400, f"Expected 400 Bad Request for capacity < 1, got {code}"

    # Items empty
    data = {"items": [], "capacity": 50}
    code, _ = post_json(url, data)
    assert code == 400, f"Expected 400 Bad Request for empty items array, got {code}"

def test_api_rate_limiting(api_server):
    url = "http://127.0.0.1:8080/solve"
    data = {"items": [{"weight": 10, "value": 60}], "capacity": 50}

    # Wait to ensure rate limit bucket is full
    time.sleep(1.5)

    def make_request():
        return post_json(url, data)[0]

    results = []
    # Send 10 requests rapidly
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())

    status_429_count = results.count(429)
    status_200_count = results.count(200)

    assert status_429_count > 0, f"Expected at least one 429 Too Many Requests status when sending 10 requests rapidly, got {results}"
    assert status_200_count <= 5, f"Expected at most 5 successful requests in a burst, got {status_200_count} (results: {results})"