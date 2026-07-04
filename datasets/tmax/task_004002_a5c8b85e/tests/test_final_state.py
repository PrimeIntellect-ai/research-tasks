# test_final_state.py

import os
import time
import json
import subprocess
import urllib.request
import pytest

def test_executable_exists():
    path = "/home/user/fast_backup"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile your C++ code?"
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_performance_and_correctness():
    # Clean up state to ensure we are testing the actual run
    if os.path.exists("/home/user/backup.tar"):
        os.remove("/home/user/backup.tar")

    try:
        # Clear redis
        subprocess.run(["redis-cli", "DEL", "backup:manifest"], check=True, capture_output=True)
    except Exception as e:
        pytest.fail(f"Failed to clear Redis key: {e}")

    # Run the executable and measure time
    start_time = time.perf_counter()
    result = subprocess.run(["/home/user/fast_backup"], capture_output=True, text=True)
    end_time = time.perf_counter()

    assert result.returncode == 0, f"Executable failed with return code {result.returncode}. Stderr: {result.stderr}"

    elapsed = end_time - start_time
    assert elapsed <= 2.0, f"Execution time {elapsed:.3f}s exceeded threshold of 2.0s."

    # Check correctness against the validation service
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/validate")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            assert data.get("status") == "success", f"Validation service reported failure: {data}"
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        pytest.fail(f"Validation service returned HTTP {e.code}: {error_body}")
    except Exception as e:
        pytest.fail(f"Failed to reach validation service or validate: {e}")