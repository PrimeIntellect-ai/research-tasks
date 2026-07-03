# test_final_state.py
import os
import subprocess
import json
import pytest

def test_crontab_configured():
    """Verify that a crontab entry exists for the operator."""
    try:
        cron_output = subprocess.check_output("crontab -l", shell=True, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("No crontab found for the user.")
    assert "operator" in cron_output, "Crontab not configured properly with operator script."

def test_manifest_exists():
    """Verify that the test manifest exists and has correct contents."""
    manifest_path = '/home/user/manifests/test-service.json'
    assert os.path.exists(manifest_path), f"Manifest file not found at {manifest_path}"
    with open(manifest_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest file is not valid JSON.")

    assert data.get("service_name") == "test-service", "Incorrect service_name in manifest."
    assert data.get("command") == "sleep 7200", "Incorrect command in manifest."
    assert data.get("replicas") == 3, "Incorrect replicas in manifest."

def test_pid_file_and_processes():
    """Verify that the PID file exists, contains exactly 3 PIDs, and they correspond to running sleep processes."""
    pid_file = '/home/user/run/test-service.pids'
    assert os.path.exists(pid_file), f"PID file not found at {pid_file}"

    with open(pid_file, 'r') as f:
        pids = [line.strip() for line in f if line.strip().isdigit()]

    assert len(pids) == 3, f"Expected exactly 3 PIDs in {pid_file}, found {len(pids)}"

    for pid in pids:
        try:
            cmd = f"ps -p {pid} -o comm="
            output = subprocess.check_output(cmd, shell=True, text=True).strip()
            assert "sleep" in output, f"Process {pid} is running but is not 'sleep' (found '{output}')"
        except subprocess.CalledProcessError:
            pytest.fail(f"Process with PID {pid} listed in the PID file is not running.")

def test_mail_file():
    """Verify that the mail spool file exists and contains the required mbox headers and body."""
    mail_file = '/home/user/mail/admin'
    assert os.path.exists(mail_file), f"Mail file not found at {mail_file}"

    with open(mail_file, 'r') as f:
        content = f.read()

    assert "From: operator@localhost" in content, "Missing 'From: operator@localhost' header in mail file."
    assert "Subject: Scaling service test-service" in content, "Missing 'Subject: Scaling service test-service' header in mail file."
    assert "Started PID" in content, "Missing 'Started PID' action in mail body."