# test_final_state.py

import os
import subprocess
import pytest

def test_proxy_service_dependencies():
    """Verify that proxy.service has the correct systemd dependencies."""
    path = "/home/user/.config/systemd/user/proxy.service"
    assert os.path.isfile(path), f"{path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert "Requires=backend.service" in content, "proxy.service is missing 'Requires=backend.service'"
    assert "After=backend.service" in content, "proxy.service is missing 'After=backend.service'"

def test_binary_compiled():
    """Verify that the C proxy was compiled to the expected location."""
    bin_path = "/home/user/health_proxy"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing. Did you compile health_proxy.c?"
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_proxy_log_exists_and_populated():
    """Verify that the new log file exists and contains data (indicating a successful request)."""
    log_path = "/home/user/logs/proxy.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Ensure the C code was updated, compiled, and a request was made."
    assert os.path.getsize(log_path) > 0, f"Log file {log_path} is empty. Did you make a successful curl request to the proxy?"

def test_services_active():
    """Verify that both user systemd services are active."""
    for svc in ["backend.service", "proxy.service"]:
        cmd = f"su - user -c 'systemctl --user is-active {svc}'"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        status = res.stdout.strip()
        assert status == "active", f"Service {svc} is not active. Current status: '{status}'. Error output: {res.stderr.strip()}"