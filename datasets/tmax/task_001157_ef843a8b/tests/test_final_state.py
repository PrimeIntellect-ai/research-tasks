# test_final_state.py
import os
import subprocess
import json
import time

def test_bashrc_env_vars():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"{bashrc_path} does not exist"

    with open(bashrc_path, "r") as f:
        content = f.read()

    # Check for METRICS_HOST
    assert "METRICS_HOST" in content and "127.0.0.1:9999" in content, "METRICS_HOST not correctly exported in .bashrc"
    assert "export METRICS_HOST" in content, "METRICS_HOST is not exported"

    # Check for LOAD_THRESHOLD
    assert "LOAD_THRESHOLD" in content and "4.0" in content, "LOAD_THRESHOLD not correctly exported in .bashrc"
    assert "export LOAD_THRESHOLD" in content, "LOAD_THRESHOLD is not exported"

def test_crontab_configured():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab"

    crontab_output = result.stdout
    expected_command = "/home/user/capacity_monitor/target/release/capacity_monitor"
    assert expected_command in crontab_output, f"Crontab does not contain the expected command: {expected_command}"
    assert "*/5 * * * *" in crontab_output, "Crontab does not schedule the task every 5 minutes"

def test_rust_binary_exists_and_executable():
    binary_path = "/home/user/capacity_monitor/target/release/capacity_monitor"
    assert os.path.exists(binary_path), f"Rust binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable"

def test_rust_binary_execution_and_log():
    binary_path = "/home/user/capacity_monitor/target/release/capacity_monitor"
    log_file = "/home/user/capacity_log.jsonl"

    # Get initial line count if file exists
    initial_lines = 0
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            initial_lines = len(f.readlines())

    # Run the binary
    env = os.environ.copy()
    env["METRICS_HOST"] = "127.0.0.1:9999"
    env["LOAD_THRESHOLD"] = "4.0"

    result = subprocess.run([binary_path], env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"Binary execution failed with output: {result.stderr}"

    assert os.path.exists(log_file), f"Log file {log_file} was not created"

    with open(log_file, "r") as f:
        lines = f.readlines()

    assert len(lines) > initial_lines, "Binary did not append a new line to the log file"

    last_line = lines[-1].strip()
    try:
        data = json.loads(last_line)
    except json.JSONDecodeError:
        pytest.fail(f"Appended line is not valid JSON: {last_line}")

    expected_keys = {"timestamp", "load_1m", "mem_avail_kb", "endpoint_reachable", "threshold_exceeded"}
    assert set(data.keys()) == expected_keys, f"JSON object missing or has extra keys. Expected {expected_keys}, got {set(data.keys())}"

    assert isinstance(data["timestamp"], int), "timestamp must be an integer"
    assert isinstance(data["load_1m"], float), "load_1m must be a float"
    assert isinstance(data["mem_avail_kb"], int), "mem_avail_kb must be an integer"
    assert isinstance(data["endpoint_reachable"], bool), "endpoint_reachable must be a boolean"
    assert isinstance(data["threshold_exceeded"], bool), "threshold_exceeded must be a boolean"

    # Check logic
    assert data["threshold_exceeded"] == (data["load_1m"] > 4.0), "threshold_exceeded logic is incorrect"

    # Verify timestamp is recent
    current_time = int(time.time())
    assert abs(current_time - data["timestamp"]) < 10, "timestamp is not close to current time"