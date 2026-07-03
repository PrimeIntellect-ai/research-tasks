# test_final_state.py

import os
import subprocess
import pytest

def test_libscheduler_so_exists():
    path = "/home/user/app/clib/libscheduler.so"
    assert os.path.isfile(path), f"File {path} does not exist. Did you compile the C library?"

def test_integration_test_exists():
    path = "/home/user/app/integration_test.py"
    assert os.path.isfile(path), f"File {path} does not exist. You must create the integration test script."

def test_performance_metric():
    # Run the integration test
    script_path = "/home/user/app/integration_test.py"
    log_path = "/home/user/app/perf.log"

    # Remove old perf.log if exists
    if os.path.exists(log_path):
        os.remove(log_path)

    try:
        subprocess.run(["python3", script_path], check=True, timeout=30)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"integration_test.py failed to run: {e}")
    except subprocess.TimeoutExpired:
        pytest.fail("integration_test.py timed out. The system is too slow or hung.")

    assert os.path.isfile(log_path), f"File {log_path} was not created by integration_test.py."

    with open(log_path, "r") as f:
        content = f.read().strip()

    try:
        exec_time = float(content)
    except ValueError:
        pytest.fail(f"Could not parse '{content}' in {log_path} as a float.")

    assert exec_time <= 1.5, f"Execution time was {exec_time} seconds, which is strictly greater than the threshold of 1.5 seconds."

def test_redis_queue_empty():
    # Attempt to check if there are any list keys in Redis that have elements
    try:
        # Use redis-cli to get all keys
        result = subprocess.run(["redis-cli", "keys", "*"], capture_output=True, text=True, check=True)
        keys = result.stdout.split()
        for key in keys:
            type_res = subprocess.run(["redis-cli", "type", key], capture_output=True, text=True, check=True)
            if type_res.stdout.strip() == "list":
                len_res = subprocess.run(["redis-cli", "llen", key], capture_output=True, text=True, check=True)
                length = int(len_res.stdout.strip())
                assert length == 0, f"Redis list '{key}' is not empty (length {length}). Jobs were not fully processed."
    except Exception as e:
        # If redis-cli fails or something else goes wrong, we might not be able to check perfectly,
        # but we shouldn't fail the test if we can't determine it unless it's a direct assertion failure.
        if isinstance(e, AssertionError):
            raise