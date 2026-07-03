# test_final_state.py
import os
import sys
import threading
import subprocess
import pytest

def test_recursion_ids():
    path = "/home/user/recursion_ids.txt"
    assert os.path.isfile(path), f"{path} does not exist. You must extract the request IDs."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["1005", "1012"]
    assert lines == expected, f"Expected {path} to contain {expected}, but got {lines}."

def test_math_service_negative_n():
    sys.path.insert(0, "/home/user")
    try:
        import math_service
    except ImportError:
        pytest.fail("Could not import math_service from /home/user")

    try:
        res1 = math_service.compute_sequence(-1)
        res2 = math_service.compute_sequence(-10)
    except RecursionError:
        pytest.fail("compute_sequence still raises RecursionError for negative inputs.")

    assert res1 == -1, f"Expected compute_sequence(-1) to return -1, got {res1}."
    assert res2 == -1, f"Expected compute_sequence(-10) to return -1, got {res2}."

def test_math_service_deadlock():
    sys.path.insert(0, "/home/user")
    import math_service

    threads = []
    exceptions = []

    def worker(req_id, n):
        try:
            math_service.process_request(req_id, n)
        except Exception as e:
            exceptions.append(e)

    # Launch concurrent requests mixing even and odd numbers to trigger any potential deadlock
    for i in range(50):
        t = threading.Thread(target=worker, args=(i, i % 4))
        threads.append(t)
        t.start()

    for t in threads:
        t.join(timeout=2.0)
        assert not t.is_alive(), "Deadlock detected: thread hung while executing process_request."

    assert not exceptions, f"Exceptions occurred during concurrent execution: {exceptions}"

def test_regression_script():
    path = "/home/user/test_math_service.py"
    assert os.path.isfile(path), f"Regression test script {path} does not exist."

    try:
        result = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {path} timed out. It may be deadlocking or taking too long.")

    assert result.returncode == 0, (
        f"Expected {path} to exit with code 0, but got {result.returncode}.\n"
        f"Stdout: {result.stdout}\nStderr: {result.stderr}"
    )