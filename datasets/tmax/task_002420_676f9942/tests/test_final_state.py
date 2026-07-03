# test_final_state.py

import os
import pytest

def test_binary_size():
    binary_path = "/home/user/health_monitor/target/release/monitor"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}"

    size = os.path.getsize(binary_path)
    threshold = 400000
    assert size <= threshold, f"Binary size is {size} bytes, which exceeds the threshold of {threshold} bytes."

def test_log_output():
    log_path = "/home/user/logs/monitor.log"
    assert os.path.isfile(log_path), f"Log file not found at {log_path}. Did you fix run_monitor.sh and run it?"

    with open(log_path, "r") as f:
        content = f.read()

    expected_text = "Connecting to 127.0.0.1:8899 with token EDGE-MIGRATE-2024"
    assert expected_text in content, f"Log file does not contain the expected output. Found: {content}"