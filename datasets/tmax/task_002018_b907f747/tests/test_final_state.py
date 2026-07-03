# test_final_state.py

import os
import json
import subprocess
import re
import pytest

def test_rust_project_exists():
    assert os.path.isfile("/home/user/latency_monitor/Cargo.toml"), "Cargo.toml not found in /home/user/latency_monitor."

def test_rust_binary_exists_and_executable():
    binary_path = "/home/user/latency_monitor/target/release/latency_monitor"
    assert os.path.isfile(binary_path), f"Release binary not found at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable."

def test_binary_execution_and_log_format():
    binary_path = "/home/user/latency_monitor/target/release/latency_monitor"
    log_path = "/home/user/latency.log"

    # Clear the log file if it exists to ensure we only read the latest run
    if os.path.exists(log_path):
        os.remove(log_path)

    # Execute the binary
    result = subprocess.run([binary_path], capture_output=True)
    assert result.returncode == 0, f"Binary execution failed with return code {result.returncode}."

    # Check log file
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 2, "Log file should contain at least two entries."

    endpoints_found = set()
    for line in lines:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Log line is not valid JSON: {line}")

        assert "endpoint" in data, "JSON log missing 'endpoint' key."
        assert "latency_ms" in data, "JSON log missing 'latency_ms' key."
        assert "success" in data, "JSON log missing 'success' key."

        assert isinstance(data["latency_ms"], int), "'latency_ms' must be an integer."
        assert isinstance(data["success"], bool), "'success' must be a boolean."

        endpoints_found.add(data["endpoint"])

    assert "8.8.8.8:53" in endpoints_found, "Endpoint 8.8.8.8:53 not found in logs."
    assert "1.1.1.1:53" in endpoints_found, "Endpoint 1.1.1.1:53 not found in logs."

def test_crontab_configuration():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    # It's possible crontab is not set for the user, but it should be
    assert result.returncode == 0, "Failed to read crontab."

    crontab_content = result.stdout
    binary_path = "/home/user/latency_monitor/target/release/latency_monitor"

    assert binary_path in crontab_content, f"Crontab does not contain the binary path {binary_path}."

    # Check for * * * * * schedule
    # A simple check for the cron schedule line
    schedule_pattern = re.compile(r"^\s*\*\s+\*\s+\*\s+\*\s+\*\s+.*" + re.escape(binary_path), re.MULTILINE)
    assert schedule_pattern.search(crontab_content), "Crontab does not have the correct '* * * * *' schedule for the binary."

def test_logrotate_configuration():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"Logrotate config not found at {conf_path}."

    with open(conf_path, "r") as f:
        content = f.read()

    # Check target
    assert "/home/user/latency.log" in content, "Logrotate config does not target /home/user/latency.log."

    # Check directives
    directives = ["size 10k", "rotate 5", "compress", "missingok", "notifempty"]
    for directive in directives:
        # Allow multiple spaces/newlines
        assert re.search(r"\b" + directive.replace(" ", r"\s+") + r"\b", content), f"Logrotate config missing directive: {directive}"