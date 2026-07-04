# test_final_state.py

import os
import time
import subprocess
import pytest

def test_settings_bin_recovered():
    path = "/home/user/monitor_env/config/settings.bin"
    assert os.path.isfile(path), f"Expected recovered file {path} does not exist."
    assert os.path.getsize(path) > 0, f"Expected {path} to contain data."

def test_uptime_monitor_runs():
    # The binary should now run successfully without library errors or missing config
    try:
        result = subprocess.run(['/app/uptime_monitor'], capture_output=True, text=True, timeout=2)
        assert result.returncode == 0, f"/app/uptime_monitor failed to run. Return code: {result.returncode}, stderr: {result.stderr}"
        assert len(result.stdout.strip()) > 0, "/app/uptime_monitor produced no output."
    except Exception as e:
        pytest.fail(f"Failed to execute /app/uptime_monitor: {e}")

def test_fast_wrapper_exists_and_executable():
    path = "/home/user/monitor_env/fast_wrapper"
    assert os.path.isfile(path), f"Expected wrapper binary {path} does not exist."
    assert os.access(path, os.X_OK), f"Expected {path} to be executable."

def test_fast_wrapper_correctness():
    # Ensure the wrapper produces the same output as the original binary
    orig_result = subprocess.run(['/app/uptime_monitor'], capture_output=True, text=True)
    wrap_result = subprocess.run(['/home/user/monitor_env/fast_wrapper'], capture_output=True, text=True)

    assert wrap_result.returncode == 0, f"fast_wrapper failed to run. stderr: {wrap_result.stderr}"
    assert orig_result.stdout.strip() == wrap_result.stdout.strip(), "fast_wrapper output does not match original binary output."

def test_fast_wrapper_speedup():
    # Measure base time
    start = time.time()
    for _ in range(100):
        subprocess.run(['/app/uptime_monitor'], stdout=subprocess.DEVNULL)
    base_time = time.time() - start

    # Measure wrapper time
    start = time.time()
    for _ in range(100):
        subprocess.run(['/home/user/monitor_env/fast_wrapper'], stdout=subprocess.DEVNULL)
    wrapper_time = time.time() - start

    # Calculate speedup
    speedup = base_time / wrapper_time

    assert speedup >= 50.0, f"Speedup factor is {speedup:.2f}, which is less than the required 50.0. Base time: {base_time:.2f}s, Wrapper time: {wrapper_time:.2f}s."