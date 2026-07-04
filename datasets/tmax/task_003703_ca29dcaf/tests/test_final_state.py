# test_final_state.py

import os
import subprocess
import pytest

def test_deploy_script_exists():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.exists(deploy_script), f"Fail: {deploy_script} does not exist."
    assert os.path.isfile(deploy_script), f"Fail: {deploy_script} is not a file."

def test_deploy_script_execution_and_idempotency():
    deploy_script = "/home/user/deploy.sh"

    # Run deployment script first time
    result1 = subprocess.run(["bash", deploy_script], capture_output=True, text=True)
    assert result1.returncode == 0, f"Fail: deploy.sh failed on first run. Stderr: {result1.stderr}"

    # Check compilation
    probe_executable = "/home/user/probe_ssh"
    assert os.path.exists(probe_executable), f"Fail: {probe_executable} executable not found."
    assert os.access(probe_executable, os.X_OK), f"Fail: {probe_executable} is not executable."

    # Check permissions of alerts.log
    alerts_log = "/home/user/alerts.log"
    assert os.path.exists(alerts_log), f"Fail: {alerts_log} was not created."
    stat_info = os.stat(alerts_log)
    perms = oct(stat_info.st_mode)[-3:]
    assert perms == "600", f"Fail: incorrect permissions on alerts.log ({perms} instead of 600)."

    # Run deployment script second time for idempotency
    result2 = subprocess.run(["bash", deploy_script], capture_output=True, text=True)
    assert result2.returncode == 0, f"Fail: deploy.sh is not idempotent (exited with non-zero on second run). Stderr: {result2.stderr}"

def test_prober_execution_and_alert():
    probe_executable = "/home/user/probe_ssh"
    alerts_log = "/home/user/alerts.log"

    # Run the prober
    result = subprocess.run([probe_executable], capture_output=True, text=True)
    assert result.returncode == 0, f"Fail: probe_ssh exited with non-zero code. Stderr: {result.stderr}"

    # Verify the alert log
    assert os.path.exists(alerts_log), f"Fail: {alerts_log} does not exist."
    with open(alerts_log, "r") as f:
        alert_content = f.read()

    expected_json = '{"event":"key_rejected","target":"jumphost"}'
    assert expected_json in alert_content, f"Fail: alerts.log does not contain the expected JSON alert. Found: {alert_content}"