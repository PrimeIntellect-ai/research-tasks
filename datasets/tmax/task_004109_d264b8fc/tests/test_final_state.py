# test_final_state.py

import os
import subprocess
import time
import statistics
import requests
import pytest

def test_server_exists():
    assert os.path.isfile("/app/server.py"), "Expected server script at /app/server.py does not exist."

def test_server_latency_and_correctness():
    """
    Starts the FastAPI server, sends 500 requests to the /solve endpoint,
    and verifies that it doesn't crash (returns 200 OK) and meets the latency requirement.
    """
    server_path = "/app/server.py"
    assert os.path.isfile(server_path), "Server script not found."

    # Start the agent's server
    proc = subprocess.Popen(["python", server_path])

    # Wait for the server to start
    time.sleep(3)

    # Check if process crashed immediately
    if proc.poll() is not None:
        pytest.fail("Server process crashed immediately upon startup.")

    try:
        latencies = []
        payload = {"matrix": [[0] * 9 for _ in range(9)]}

        # We need to ensure the server is actually up before the 500 requests
        # Let's do a quick health check / retry logic for the first request
        max_retries = 5
        for attempt in range(max_retries):
            try:
                resp = requests.post("http://127.0.0.1:8000/solve", json=payload, timeout=2)
                if resp.status_code == 200:
                    break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        else:
            pytest.fail("Could not connect to the server at http://127.0.0.1:8000/solve after multiple retries.")

        # Run the benchmark
        for i in range(500):
            try:
                resp = requests.post("http://127.0.0.1:8000/solve", json=payload, timeout=5)
            except requests.exceptions.RequestException as e:
                pytest.fail(f"Request {i+1}/500 failed with exception: {e}. The server likely crashed due to a segfault.")

            assert resp.status_code == 200, f"Request {i+1}/500 returned status code {resp.status_code}. Expected 200 OK."
            latencies.append(resp.elapsed.total_seconds() * 1000)

        avg_latency = statistics.mean(latencies)
        assert avg_latency <= 15.0, f"Average latency {avg_latency:.2f}ms > 15.0ms threshold. The C extension might not be optimized."

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()