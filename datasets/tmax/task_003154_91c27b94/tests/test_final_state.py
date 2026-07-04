# test_final_state.py
import os
import re
import time
import subprocess
import pytest

def get_api_key_from_git():
    """Extract the deleted API key from the git history to avoid hardcoding."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-p", "--all"], 
            cwd="/app/vendored/liblog-anomaly", 
            text=True
        )
        # Look for the removed line defining TEST_API_KEY
        match = re.search(r'^-\s*#define\s+TEST_API_KEY\s+"([^"]+)"', out, re.MULTILINE)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "A9F3J882MD710X2P"  # Fallback to the truth value

def get_trigger_log_from_data():
    """Extract the specific malformed log line from the crash logs."""
    try:
        with open("/app/data/crash_logs.txt", "r") as f:
            for line in f:
                if "cpu_temp=85.33333333333333" in line:
                    return line.strip()
    except Exception:
        pass
    return "[2023-10-12 14:00:00] ERROR cpu_temp=85.33333333333333"  # Fallback

def test_api_key_recovered():
    api_key_file = "/home/user/api_key.txt"
    assert os.path.isfile(api_key_file), f"File {api_key_file} does not exist."

    with open(api_key_file, "r") as f:
        key = f.read().strip()

    expected_key = get_api_key_from_git()
    assert key == expected_key, f"Incorrect API Key recovered. Expected {expected_key}, got {key}"

def test_trigger_log_isolated():
    trigger_file = "/home/user/trigger_log.txt"
    assert os.path.isfile(trigger_file), f"File {trigger_file} does not exist."

    with open(trigger_file, "r") as f:
        trigger = f.read().strip()

    expected_trigger = get_trigger_log_from_data()
    assert trigger == expected_trigger, "Failed to isolate the exact trigger log line."

def test_anomaly_detector_runtime():
    binary_path = "/app/vendored/liblog-anomaly/anomaly_detector"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} not found. Did you run 'make'?"

    start_time = time.time()
    try:
        result = subprocess.run(
            [binary_path, "/app/data/benchmark.log"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5.0
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Metric threshold failed: binary execution timed out after 5.0 seconds. The infinite loop is likely not fixed.")

    end_time = time.time()
    runtime_seconds = end_time - start_time

    assert result.returncode == 0, f"Binary failed to execute or returned non-zero exit code: {result.returncode}."
    assert runtime_seconds <= 0.5, f"Metric threshold failed: runtime_seconds ({runtime_seconds:.3f}s) > 0.5s"