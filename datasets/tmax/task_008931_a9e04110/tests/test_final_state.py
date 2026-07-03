# test_final_state.py
import os
import socket
import subprocess
import urllib.request
import pytest

OBSERVABILITY_DIR = "/home/user/observability"
BACKUPS_DIR = os.path.join(OBSERVABILITY_DIR, "backups")
BACKUP_FILE = os.path.join(BACKUPS_DIR, "service_b.conf.bak")
SERVICE_B_CONF = os.path.join(OBSERVABILITY_DIR, "service_b.conf")
ALERT_CONF = os.path.join(OBSERVABILITY_DIR, "alert.conf")
MONITOR_SCRIPT = os.path.join(OBSERVABILITY_DIR, "monitor.sh")
DASHBOARD_LOG = os.path.join(OBSERVABILITY_DIR, "dashboard.log")
CRON_FILE = os.path.join(OBSERVABILITY_DIR, "cron_schedule.txt")

def test_backup_created():
    assert os.path.isdir(BACKUPS_DIR), f"Backup directory {BACKUPS_DIR} was not created."
    assert os.path.isfile(BACKUP_FILE), f"Backup file {BACKUP_FILE} does not exist."
    with open(BACKUP_FILE, "r") as f:
        content = f.read()
    assert "BIND_PORT=8083" in content, f"Backup file does not contain the original BIND_PORT=8083."

def test_service_b_conf_updated():
    assert os.path.isfile(SERVICE_B_CONF), f"File {SERVICE_B_CONF} does not exist."
    with open(SERVICE_B_CONF, "r") as f:
        content = f.read()
    assert "BIND_PORT=8082" in content, "BIND_PORT was not updated to 8082 in service_b.conf."

def test_alert_conf_updated():
    assert os.path.isfile(ALERT_CONF), f"File {ALERT_CONF} does not exist."
    with open(ALERT_CONF, "r") as f:
        content = f.read()
    assert "SMTP_PORT=1025" in content, "SMTP_PORT was not updated to 1025 in alert.conf."

def test_service_b_running():
    # Check if something is listening on port 8082
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 8082))
        assert result == 0, "Service B is not listening on port 8082. Did you run start_service_b.sh?"

def test_monitor_script_logic():
    assert os.path.isfile(MONITOR_SCRIPT), f"Monitor script {MONITOR_SCRIPT} does not exist."
    assert os.access(MONITOR_SCRIPT, os.X_OK), f"Monitor script {MONITOR_SCRIPT} is not executable."

    # Run the monitor script
    if os.path.exists(DASHBOARD_LOG):
        os.remove(DASHBOARD_LOG)

    result = subprocess.run([MONITOR_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, "Monitor script execution failed."

    assert os.path.isfile(DASHBOARD_LOG), f"Dashboard log {DASHBOARD_LOG} was not created by the monitor script."
    with open(DASHBOARD_LOG, "r") as f:
        content = f.read()
    assert "SERVICE_B_UP" in content, "Monitor script did not append 'SERVICE_B_UP' to the dashboard log when the service is up."

def test_cron_schedule():
    assert os.path.isfile(CRON_FILE), f"Cron schedule file {CRON_FILE} does not exist."
    with open(CRON_FILE, "r") as f:
        content = f.read().strip()
    expected = f"* * * * * {MONITOR_SCRIPT}"
    assert content == expected, f"Cron schedule file does not contain the exact expected expression. Got: '{content}', Expected: '{expected}'"