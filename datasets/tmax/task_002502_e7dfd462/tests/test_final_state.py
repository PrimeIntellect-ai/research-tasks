# test_final_state.py

import os
import time
import json
import urllib.request
import threading
import subprocess
import pytest
import math

FIXED_SERVICE_PATH = "/home/user/fixed_math_service.py"
PORT = 8080
URL = f"http://127.0.0.1:{PORT}"

@pytest.fixture(scope="module")
def server_process():
    assert os.path.exists(FIXED_SERVICE_PATH), f"File {FIXED_SERVICE_PATH} not found."

    # Start the server
    proc = subprocess.Popen(["python3", FIXED_SERVICE_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for server to start
    started = False
    for _ in range(20):
        try:
            urllib.request.urlopen(URL, timeout=1)
            started = True
            break
        except Exception:
            time.sleep(0.5)

    if not started:
        proc.terminate()
        pytest.fail("Server did not start or become reachable on port 8080.")

    yield proc

    proc.terminate()
    proc.wait(timeout=2)

def send_request(data):
    req = urllib.request.Request(URL, 
                                 data=json.dumps(data).encode(), 
                                 headers={'Content-Type': 'application/json'},
                                 method='POST')
    response = urllib.request.urlopen(req, timeout=5)
    return json.loads(response.read().decode())

def test_comma_parsing(server_process):
    try:
        res = send_request({"values": ["1,000.5", "2,000.5"]})
        assert "std_dev" in res, "Response missing 'std_dev' key."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Server returned HTTP {e.code} for comma-separated values. Parsing failed.")
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

def test_numerical_instability(server_process):
    try:
        res = send_request({"values": ["100000000.01", "100000000.02"]})
        assert "std_dev" in res, "Response missing 'std_dev' key."
        std_dev = res["std_dev"]
        assert not math.isnan(std_dev), "Calculated standard deviation is NaN."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Server returned HTTP {e.code} for close large values. Math domain error likely occurred.")
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

def test_concurrency(server_process):
    errors = []

    def worker():
        try:
            for _ in range(10):
                send_request({"values": [1, 2, 3]})
        except Exception as e:
            errors.append(e)

    threads = []
    for _ in range(20):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert not errors, f"Concurrency test encountered errors: {errors[0]}"

    # Final request to check if server is still alive and responsive
    try:
        res = send_request({"values": [4, 5, 6]})
        assert "std_dev" in res, "Response missing 'std_dev' key."
    except Exception as e:
        pytest.fail(f"Server failed to respond after concurrent load: {e}")