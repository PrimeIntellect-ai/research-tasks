# test_final_state.py

import os
import stat
import subprocess
import json
import urllib.request
import urllib.error
import ssl
import pytest

WEBHOOK_DIR = "/home/user/webhook"
CERT_FILE = os.path.join(WEBHOOK_DIR, "cert.pem")
KEY_FILE = os.path.join(WEBHOOK_DIR, "key.pem")
SERVER_SCRIPT = os.path.join(WEBHOOK_DIR, "server.py")
ALERTS_LOG = os.path.join(WEBHOOK_DIR, "alerts.log")
MONITOR_SCRIPT = "/home/user/monitor.sh"
CRON_CONF = "/home/user/cron.conf"

def test_certificates_exist():
    """Check that the self-signed certificate and key exist."""
    assert os.path.isfile(CERT_FILE), f"Certificate file {CERT_FILE} is missing."
    assert os.path.isfile(KEY_FILE), f"Key file {KEY_FILE} is missing."

def test_webhook_script_exists():
    """Check that the webhook server script exists and contains ssl import."""
    assert os.path.isfile(SERVER_SCRIPT), f"Server script {SERVER_SCRIPT} is missing."
    with open(SERVER_SCRIPT, "r") as f:
        content = f.read()
    assert "ssl" in content, "Server script does not seem to import 'ssl'."

def test_monitor_script_executable_and_content():
    """Check that monitor.sh exists, is executable, and contains curl commands."""
    assert os.path.isfile(MONITOR_SCRIPT), f"Monitor script {MONITOR_SCRIPT} is missing."

    st = os.stat(MONITOR_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{MONITOR_SCRIPT} is not executable."

    with open(MONITOR_SCRIPT, "r") as f:
        content = f.read()
    assert "curl" in content, "Monitor script does not contain 'curl'."
    assert "8443/alert" in content, "Monitor script does not post to the webhook on 8443."

def test_cron_job_configured():
    """Check that the crontab contains the correct schedule for monitor.sh."""
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it configured?")

    assert "* * * * * /home/user/monitor.sh" in output, "Crontab does not contain the expected cron job for monitor.sh."

def test_alerts_log_content():
    """Check that alerts.log contains the correct alert for service 8003."""
    assert os.path.isfile(ALERTS_LOG), f"Alerts log {ALERTS_LOG} is missing."

    with open(ALERTS_LOG, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) >= 1, "Alerts log is empty."

    # Parse the last line as JSON to be robust against spacing
    try:
        last_alert = json.loads(lines[-1])
    except json.JSONDecodeError:
        pytest.fail("The last line in alerts.log is not valid JSON.")

    assert last_alert.get("service") == "service_8003", "Expected alert for 'service_8003'."
    assert last_alert.get("status") == "down", "Expected status 'down'."

def test_webhook_server_running():
    """Check that the webhook server is running and accepts POST requests."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    data = json.dumps({"service": "test_service", "status": "down"}).encode('utf-8')
    req = urllib.request.Request("https://127.0.0.1:8443/alert", data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.getcode() == 200, "Webhook server did not return HTTP 200 OK."
    except Exception as e:
        pytest.fail(f"Failed to connect and POST to the webhook server on 8443: {e}")