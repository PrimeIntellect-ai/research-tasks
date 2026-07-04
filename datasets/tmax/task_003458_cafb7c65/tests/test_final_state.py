# test_final_state.py

import os
import time
import requests
import base64
from concurrent.futures import ThreadPoolExecutor
import pytest

@pytest.fixture(scope="module", autouse=True)
def wait_for_server():
    """Wait for the server to be ready before running any tests."""
    ready_file = "/home/user/app/server_ready.log"
    wait_time = 0
    ready = False
    while wait_time < 30:
        if os.path.exists(ready_file):
            with open(ready_file, "r") as f:
                if "READY" in f.read():
                    ready = True
                    break
        time.sleep(1)
        wait_time += 1
    assert ready, "Server never became ready (did not write 'READY' to /home/user/app/server_ready.log within 30 seconds)."

def test_correctness():
    """Verify that the API returns the correct JSON format and properly encoded JPEG data."""
    try:
        resp = requests.get("http://127.0.0.1:8000/api/v1/frame/15", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "frame" in data, "Response JSON missing 'frame' key"
    assert "data" in data, "Response JSON missing 'data' key"
    assert data["frame"] == 15, f"Expected frame 15, got {data['frame']}"

    reversed_b64 = data["data"]
    actual_b64 = reversed_b64[::-1]

    try:
        jpeg_bytes = base64.b64decode(actual_b64, validate=True)
    except Exception as e:
        pytest.fail(f"Failed to decode base64 data: {e}. Ensure the data is a valid reversed Base64 string.")

    assert jpeg_bytes.startswith(b'\xff\xd8'), "Decoded data is not a valid JPEG (missing JPEG magic bytes '\\xff\\xd8')"

def test_performance_rps():
    """Benchmark the API to ensure it meets the minimum Requests Per Second (RPS) threshold."""
    num_requests = 300
    start_time = time.time()

    def fetch(i):
        try:
            # Request random frames between 0 and 89 (3 seconds at 30fps)
            r = requests.get(f"http://127.0.0.1:8000/api/v1/frame/{i % 90}", timeout=5)
            return r.status_code
        except Exception:
            return 500

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch, range(num_requests)))

    end_time = time.time()

    successes = [r for r in results if r == 200]
    success_rate = len(successes) / num_requests
    assert success_rate >= 0.95, f"Too many failed requests during load test. Success rate: {success_rate*100:.1f}% (Expected >= 95%)"

    duration = end_time - start_time
    rps = num_requests / duration

    assert rps >= 150, f"Performance metric failed: achieved {rps:.2f} RPS, threshold is >= 150 RPS. Ensure frames are pre-extracted or cached."