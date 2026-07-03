# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
import json
import pytest
import numpy as np
from scipy.io import wavfile

def test_compiled_libraries_exist():
    assert os.path.exists("/app/c_filter/libfilter.so"), "Missing libfilter.so"
    assert os.path.exists("/app/cpp_core/libcore.so"), "Missing libcore.so"
    assert os.path.exists("/app/run_server.sh"), "Missing /app/run_server.sh"

def test_server_metrics_and_rate_limiting():
    # Ensure the script is executable
    os.chmod("/app/run_server.sh", 0o755)

    # Start the server
    server_proc = subprocess.Popen(["bash", "/app/run_server.sh"])

    # Wait for the server to be ready
    server_up = False
    for _ in range(20):
        try:
            # Just check if the port is open and responding to anything
            urllib.request.urlopen("http://127.0.0.1:8000/", timeout=1)
            server_up = True
            break
        except Exception:
            time.sleep(0.5)

    # Even if we get a 404 on root, the port is open. If connection refused, it's not up.
    time.sleep(1) # Give it a bit more time to fully initialize

    try:
        url = "http://127.0.0.1:8000/process"
        # The prompt says it accepts a file path. We'll try a standard JSON body.
        payload = json.dumps({"file_path": "/app/fixture_audio.wav"}).encode('utf-8')
        headers = {'Content-Type': 'application/json'}

        latencies = []
        status_codes = []
        responses = []

        for i in range(6):
            req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
            start_time = time.time()
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    latencies.append(time.time() - start_time)
                    status_codes.append(response.getcode())
                    if i == 0:
                        responses.append(response.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                latencies.append(time.time() - start_time)
                status_codes.append(e.code)
            except Exception as e:
                pytest.fail(f"Request failed: {e}")

        # 1. Check Rate Limiter
        assert len(status_codes) == 6, "Did not complete 6 requests"
        assert status_codes[5] == 429, f"Expected HTTP 429 Too Many Requests on the 6th request, got {status_codes[5]}"

        # 2. Check Speedup (Metric Threshold)
        assert latencies[0] <= 0.20, f"Latency metric failed: {latencies[0]:.3f}s > threshold 0.20s"

        # 3. Correctness (MSE) - basic check if response is valid JSON array
        if responses:
            try:
                data = json.loads(responses[0])
                # If the agent returned a dict with the array, extract it
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, list):
                            data = v
                            break
                assert isinstance(data, list), "Expected API to return a JSON array of processed audio"
                assert len(data) > 0, "Returned audio array is empty"
            except json.JSONDecodeError:
                pytest.fail("Failed to decode JSON response from /process")

    finally:
        server_proc.terminate()
        server_proc.wait(timeout=5)