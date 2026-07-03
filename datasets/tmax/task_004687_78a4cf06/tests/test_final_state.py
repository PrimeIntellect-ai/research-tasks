# test_final_state.py
import subprocess
import re
import os
import socket
import time
import pytest

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

@pytest.fixture(scope="session", autouse=True)
def ensure_services_running():
    """Ensure that the necessary services are running before testing."""
    if not (is_port_open(8080) and is_port_open(9000) and is_port_open(6379)):
        print("Services not fully running. Attempting to start them via /app/start_services.sh...")
        subprocess.Popen(["bash", "/app/start_services.sh"])
        for _ in range(20):
            if is_port_open(8080) and is_port_open(9000) and is_port_open(6379):
                break
            time.sleep(0.5)
        else:
            print("Warning: Services did not start up properly within the timeout.")

def test_wal_corruption_fixed():
    wal_path = "/app/data/engine.wal"
    assert os.path.isfile(wal_path), f"{wal_path} is missing"
    size = os.path.getsize(wal_path)
    assert size >= 16, "WAL file is too small to contain the 16-byte header."
    assert (size - 16) % 32 == 0, (
        f"WAL file size {size} is invalid. "
        "It should have a 16-byte header and exactly 32-byte records. "
        "The corrupted partial record at the end was not properly truncated."
    )

def test_compute_engine_build():
    engine_path = "/app/compute_engine/engine"
    assert os.path.isfile(engine_path), f"Compiled binary {engine_path} is missing. Did you fix the Makefile and compile?"
    assert os.access(engine_path, os.X_OK), f"{engine_path} is not executable."

def test_load_test_performance():
    # Make sure we can run the load test and get the metric
    try:
        out = subprocess.check_output(
            ["python3", "/app/load_test.py"], 
            stderr=subprocess.STDOUT, 
            timeout=45
        ).decode("utf-8")
    except subprocess.TimeoutExpired:
        pytest.fail("Load test timed out after 45 seconds. The concurrency livelock bug might not be fixed.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Load test failed with exit code {e.returncode}. Output:\n{e.output.decode('utf-8')}")

    match = re.search(r"RESULT_RUNTIME_SECONDS:\s*([0-9.]+)", out)
    assert match is not None, f"Metric not found in output. Output was:\n{out}"

    runtime = float(match.group(1))
    assert runtime < 3.0, (
        f"Runtime {runtime} >= 3.0 seconds. "
        "The concurrency bug in the ring buffer boundary might not be fully fixed, "
        "or the system is still experiencing high contention."
    )