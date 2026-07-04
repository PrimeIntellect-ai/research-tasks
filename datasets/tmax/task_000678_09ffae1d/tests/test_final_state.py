# test_final_state.py

import os
import subprocess
import pytest

def test_quota_updated_log():
    path = "/home/user/quota_updated.log"
    assert os.path.isfile(path), f"File {path} is missing. The expect script may not have run successfully."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "ops:13600", f"Expected 'ops:13600' in {path}, but found '{content}'"

def test_expect_script_exists():
    path = "/home/user/update_quota.exp"
    assert os.path.isfile(path), f"File {path} is missing."

def test_configure_alerts_script_exists():
    path = "/home/user/configure_alerts.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_capacity_alerts_conf():
    path = "/home/user/capacity_alerts.conf"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    assert "ALERT_GROUP=ops" in lines, f"'ALERT_GROUP=ops' not found in {path}"
    assert "THRESHOLD=13600" in lines, f"'THRESHOLD=13600' not found in {path}"

def test_configure_alerts_idempotency():
    path = "/home/user/capacity_alerts.conf"
    script = "/home/user/configure_alerts.sh"

    # Run the script again to test idempotency
    result = subprocess.run([script], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script} failed on second run."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    alert_group_count = lines.count("ALERT_GROUP=ops")
    threshold_count = lines.count("THRESHOLD=13600")

    assert alert_group_count == 1, f"Idempotency failed: 'ALERT_GROUP=ops' appears {alert_group_count} times."
    assert threshold_count == 1, f"Idempotency failed: 'THRESHOLD=13600' appears {threshold_count} times."