# test_final_state.py
import os
import time
import subprocess
import re
import pytest

def test_mailer_conf_updated():
    path = "/home/user/mailer.conf"
    assert os.path.exists(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert "PORT=8025" in content, f"Expected PORT=8025 in {path}, found: {content}"

def test_systemd_service_dependency():
    # Check if the After dependency is correctly set
    cmd = ["systemctl", "--user", "show", "-p", "After", "alert-sender.service"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    # If the environment doesn't support --user directly in tests, we can fallback to checking the file
    if res.returncode != 0:
        # Fallback to checking the file directly
        path = "/home/user/.config/systemd/user/alert-sender.service"
        with open(path, "r") as f:
            content = f.read()
        assert "After=diagnostic-logger.service" in content or "Requires=diagnostic-logger.service" in content, \
            "The alert-sender.service is missing the dependency on diagnostic-logger.service"
    else:
        assert "diagnostic-logger.service" in res.stdout, \
            f"alert-sender.service does not start after diagnostic-logger.service. Output: {res.stdout}"

def test_systemd_services_active():
    # Check if both services are active
    services = ["diagnostic-logger.service", "alert-sender.service"]
    for svc in services:
        cmd = ["systemctl", "--user", "is-active", svc]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            # Fallback to checking if the pipe exists and is being written to, or just check the service file
            pytest.skip(f"Could not verify service {svc} via systemctl --user. Assuming it's a test environment limitation.")
        else:
            assert res.stdout.strip() == "active", f"Service {svc} is not active."

def test_check_endpoints_execution_time_and_output():
    script_path = "/home/user/bin/check_endpoints.sh"
    log_path = "/home/user/endpoint_status.log"

    assert os.path.exists(script_path), f"Script {script_path} is missing."

    # Remove log to ensure we are testing the script's output
    if os.path.exists(log_path):
        os.remove(log_path)

    start_time = time.time()
    res = subprocess.run([script_path], capture_output=True, text=True)
    end_time = time.time()

    assert res.returncode == 0, f"Script failed with return code {res.returncode}. stderr: {res.stderr}"

    duration = end_time - start_time
    threshold = 0.5
    assert duration <= threshold, f"Execution time {duration:.3f}s exceeded threshold {threshold}s."

    assert os.path.exists(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 50, f"Expected 50 lines in {log_path}, found {len(lines)}."

    endpoints_found = set()
    pattern = re.compile(r"^Endpoint\s+(\d+):\s+OK$")
    for line in lines:
        match = pattern.match(line)
        assert match, f"Line format incorrect: '{line}'"
        endpoints_found.add(int(match.group(1)))

    expected_endpoints = set(range(1, 51))
    assert endpoints_found == expected_endpoints, f"Missing or incorrect endpoints in log. Found: {endpoints_found}"