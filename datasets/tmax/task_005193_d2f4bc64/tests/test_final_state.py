# test_final_state.py

import os
import subprocess
import time
import requests
import pytest
import concurrent.futures

APP_DIR = "/home/user/app"

@pytest.fixture(scope="session", autouse=True)
def setup_services():
    """Execute start.sh and wait for the HTTP gateway to become available."""
    start_script = os.path.join(APP_DIR, "start.sh")

    # Execute the start script
    proc = subprocess.run(
        [start_script],
        cwd=APP_DIR,
        capture_output=True,
        text=True
    )
    assert proc.returncode == 0, f"start.sh failed with exit code {proc.returncode}.\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"

    # Wait for the gateway to be responsive
    url = "http://127.0.0.1:8080/process"
    max_retries = 30
    for i in range(max_retries):
        try:
            # Send a dummy request to check if the service is up
            res = requests.post(url, json={"client_id": "warmup", "input_data": "test"})
            if res.status_code in (200, 429, 500):
                break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    else:
        pytest.fail("Python gateway did not become responsive on 127.0.0.1:8080 within the timeout.")

def test_basic_processing():
    """Test that the service correctly processes data using the C library."""
    url = "http://127.0.0.1:8080/process"
    payload = {"client_id": "tester", "input_data": "world"}

    response = requests.post(url, json=payload, timeout=5)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "output_data" in data, f"Response JSON missing 'output_data': {data}"
    assert data["output_data"] == "PROCESSED:world", f"Unexpected output_data: {data['output_data']}"

def test_rate_limiting():
    """Test that the rate limit of 3 requests per second per client_id is enforced."""
    url = "http://127.0.0.1:8080/process"
    client_id = "rate_limit_tester"
    payload = {"client_id": client_id, "input_data": "world"}

    def make_request():
        return requests.post(url, json=payload, timeout=5)

    # Send 5 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(5)]
        responses = [f.result() for f in futures]

    status_codes = [r.status_code for r in responses]

    successes = status_codes.count(200)
    # The prompt mentions HTTP 429, but we also accept 500 in case the gateway doesn't map gRPC codes perfectly
    failures = len([c for c in status_codes if c != 200])

    assert successes == 3, f"Expected exactly 3 successful requests, got {successes}. Status codes: {status_codes}"
    assert failures == 2, f"Expected exactly 2 rate-limited requests, got {failures}. Status codes: {status_codes}"

    # Verify that the failures are 429s (or at least mapped as errors)
    for code in status_codes:
        if code != 200:
            assert code in (429, 500), f"Expected rate limit error code to be 429 (or 500), got {code}"