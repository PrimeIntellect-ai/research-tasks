# test_final_state.py

import os
import subprocess
import pytest

def test_deploy_script_exists_and_executable():
    path = "/home/user/deploy_cost_monitor.sh"
    assert os.path.exists(path), f"Deployment script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"Deployment script {path} is not executable."

def test_bash_profile_idempotency():
    path = "/home/user/.bash_profile"
    assert os.path.exists(path), f"{path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    rate_count = content.count("FINOPS_RATE")
    limit_count = content.count("FINOPS_LIMIT")

    assert rate_count >= 1, "FINOPS_RATE is not set in .bash_profile."
    assert limit_count >= 1, "FINOPS_LIMIT is not set in .bash_profile."

def test_python_script_exists():
    path = "/home/user/calculate_costs.py"
    assert os.path.exists(path), f"Python script {path} was not created."
    assert os.path.isfile(path), f"{path} is not a file."

def test_execution_and_idempotency():
    script_path = "/home/user/deploy_cost_monitor.sh"
    log_path = "/home/user/finops_alerts.log"
    profile_path = "/home/user/.bash_profile"

    # Read initial profile state
    with open(profile_path, "r") as f:
        initial_profile = f.read()

    # Run the script again
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute on subsequent run: {result.stderr}"

    # Check profile idempotency (should not have changed or at least not added duplicate lines)
    with open(profile_path, "r") as f:
        final_profile = f.read()

    assert initial_profile == final_profile or final_profile.count("FINOPS_RATE=0.15") == 1, \
        "The script is not idempotent: .bash_profile was modified on subsequent runs with duplicate entries."

    # Check alerts log
    assert os.path.exists(log_path), f"Alert log {log_path} does not exist."
    with open(log_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) >= 2, "Alert log should have multiple lines after running the script multiple times."
    expected_alert = "[ALERT] Cost exceeds limit: $60.00 (> $50.00) - Notifying admin@local"
    assert lines[-1] == expected_alert, f"Alert log line does not match expected format. Got: {lines[-1]}"
    assert lines[-2] == expected_alert, f"Alert log line does not match expected format. Got: {lines[-2]}"