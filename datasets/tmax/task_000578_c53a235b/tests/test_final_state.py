# test_final_state.py

import os
import time
import urllib.request
import urllib.error
import pytest

def test_pen_c_fixed():
    """Check that pen.c no longer contains the deliberate latency perturbation."""
    pen_c_path = '/app/pen-0.34.1/pen.c'
    assert os.path.isfile(pen_c_path), f"Source file {pen_c_path} does not exist."
    with open(pen_c_path, 'r') as f:
        content = f.read()
    assert 'usleep(200000);' not in content, "The deliberate latency perturbation 'usleep(200000);' is still present in pen.c."

def test_pen_installed():
    """Check that pen is compiled and installed to /home/user/bin/pen."""
    pen_bin = '/home/user/bin/pen'
    assert os.path.isfile(pen_bin), f"Compiled binary not found at {pen_bin}."
    assert os.access(pen_bin, os.X_OK), f"Binary at {pen_bin} is not executable."

def test_monitor_script_exists():
    """Check that the monitor script exists and is executable."""
    monitor_script = '/home/user/monitor.sh'
    assert os.path.isfile(monitor_script), f"Monitor script not found at {monitor_script}."
    assert os.access(monitor_script, os.X_OK), f"Monitor script at {monitor_script} is not executable."

def test_backends_running():
    """Check that backend servers are running on ports 8001, 8002, 8003."""
    for port in [8001, 8002, 8003]:
        try:
            req = urllib.request.urlopen(f"http://127.0.0.1:{port}", timeout=1)
            assert req.getcode() == 200, f"Backend on port {port} returned status {req.getcode()}."
        except Exception as e:
            pytest.fail(f"Could not connect to backend server on port {port}: {e}")

def test_load_balancer_throughput():
    """Check that the load balancer is running on 8080 and meets the RPS threshold."""
    # First, verify it's up
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080", timeout=2)
        assert req.getcode() == 200, f"Load balancer returned status {req.getcode()}."
    except Exception as e:
        pytest.fail(f"Could not connect to load balancer on port 8080: {e}")

    # Measure RPS
    num_requests = 1000
    start_time = time.time()
    success_count = 0
    for _ in range(num_requests):
        try:
            req = urllib.request.urlopen("http://127.0.0.1:8080", timeout=1)
            req.read()
            if req.getcode() == 200:
                success_count += 1
        except Exception:
            pass
    end_time = time.time()

    assert success_count > 0, "All requests to the load balancer failed during benchmark."

    duration = end_time - start_time
    rps = success_count / duration

    assert rps >= 500, f"Throughput is too low: {rps:.2f} RPS. Expected >= 500 RPS."