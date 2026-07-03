# test_final_state.py

import os
import re
import stat
import pytest

def test_health_check_binary_exists_and_executable():
    """Verify that the compiled C++ monitor exists and is executable."""
    binary_path = "/home/user/bin/health_check"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_env_blue_sh_exists_and_correct():
    """Verify env_blue.sh exists and exports the correct port."""
    env_path = "/home/user/env_blue.sh"
    assert os.path.isfile(env_path), f"{env_path} does not exist."
    with open(env_path, "r") as f:
        content = f.read()
    assert re.search(r"export\s+HEALTH_PORT\s*=\s*[\"']?9001[\"']?", content), f"{env_path} does not properly export HEALTH_PORT=9001."

def test_env_green_sh_exists_and_correct():
    """Verify env_green.sh exists and exports the correct port."""
    env_path = "/home/user/env_green.sh"
    assert os.path.isfile(env_path), f"{env_path} does not exist."
    with open(env_path, "r") as f:
        content = f.read()
    assert re.search(r"export\s+HEALTH_PORT\s*=\s*[\"']?9002[\"']?", content), f"{env_path} does not properly export HEALTH_PORT=9002."

def test_deploy_monitor_sh_exists_and_executable():
    """Verify deploy_monitor.sh exists and is executable."""
    script_path = "/home/user/deploy_monitor.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_deployment_alerts_log():
    """Verify the contents of deployment_alerts.log."""
    log_path = "/home/user/deployment_alerts.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you run the deploy_monitor.sh script?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_blue = "[INFO] Deployment blue healthy on port 9001"
    expected_green = "[CRITICAL] Deployment green failed network check on port 9002"

    assert any(expected_blue in line for line in lines), f"Log does not contain expected success message for blue. Found: {lines}"
    assert any(expected_green in line for line in lines), f"Log does not contain expected failure message for green. Found: {lines}"