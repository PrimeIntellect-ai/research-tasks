# test_final_state.py

import os
import subprocess
import time
import urllib.request
import ssl
import tarfile
import pytest
import json

DEPLOY_SCRIPT = "/home/user/deploy.py"
DEPLOY_LOG = "/home/user/deploy.log"
BACKUP_ARCHIVE = "/home/user/backups/app_backup.tar.gz"
CERT_FILE = "/home/user/certs/cert.pem"
KEY_FILE = "/home/user/certs/key.pem"
SERVER_SCRIPT = "/home/user/app_v2/server.py"
FORWARD_SCRIPT = "/home/user/forward.sh"

@pytest.fixture(scope="module", autouse=True)
def execute_deployment():
    assert os.path.isfile(DEPLOY_SCRIPT), f"Deployment script {DEPLOY_SCRIPT} not found."
    assert os.access(DEPLOY_SCRIPT, os.X_OK), f"Deployment script {DEPLOY_SCRIPT} is not executable."

    # First execution
    result1 = subprocess.run([DEPLOY_SCRIPT], capture_output=True, text=True)
    assert result1.returncode == 0, f"First execution of deploy.py failed:\n{result1.stderr}"

    # Second execution (Idempotency check)
    result2 = subprocess.run([DEPLOY_SCRIPT], capture_output=True, text=True)
    assert result2.returncode == 0, f"Second execution of deploy.py failed:\n{result2.stderr}"

    # Start the server and forwarder
    server_proc = subprocess.Popen(["python3", SERVER_SCRIPT])
    forward_proc = subprocess.Popen(["bash", FORWARD_SCRIPT])

    # Give services time to start
    time.sleep(2)

    yield

    # Cleanup processes
    server_proc.terminate()
    forward_proc.terminate()
    server_proc.wait()
    forward_proc.wait()

def test_deploy_log_contents():
    assert os.path.isfile(DEPLOY_LOG), f"Log file {DEPLOY_LOG} not found."
    with open(DEPLOY_LOG, "r") as f:
        log_content = f.read().strip().splitlines()

    expected_logs = ["BACKUP_CREATED", "CERTS_GENERATED", "BACKUP_EXISTS", "CERTS_EXIST"]
    assert log_content == expected_logs, f"Log file contents do not match expected idempotency sequence. Got: {log_content}"

def test_backup_archive_exists_and_valid():
    assert os.path.isfile(BACKUP_ARCHIVE), f"Backup archive {BACKUP_ARCHIVE} not found."
    assert tarfile.is_tarfile(BACKUP_ARCHIVE), f"{BACKUP_ARCHIVE} is not a valid tar archive."

    with tarfile.open(BACKUP_ARCHIVE, "r:gz") as tar:
        names = tar.getnames()
        # Check if the data.txt from app_v1 is in the archive
        has_data = any(name.endswith("data.txt") for name in names)
        assert has_data, f"Backup archive does not contain data.txt from app_v1. Contents: {names}"

def test_tls_certificates_exist():
    assert os.path.isfile(CERT_FILE), f"Certificate file {CERT_FILE} not found."
    assert os.path.isfile(KEY_FILE), f"Key file {KEY_FILE} not found."

def test_server_https_endpoint():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:8443/status"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            assert response.getheader("Content-Type") == "application/json", "Expected Content-Type: application/json"
            data = json.loads(response.read().decode("utf-8"))
            assert data == {"version": "v2", "status": "ok"}, f"Unexpected JSON response: {data}"
    except Exception as e:
        pytest.fail(f"Failed to connect to or read from {url}: {e}")

def test_forwarder_https_endpoint():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:8080/status"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            assert response.getheader("Content-Type") == "application/json", "Expected Content-Type: application/json"
            data = json.loads(response.read().decode("utf-8"))
            assert data == {"version": "v2", "status": "ok"}, f"Unexpected JSON response: {data}"
    except Exception as e:
        pytest.fail(f"Failed to connect to or read from forwarded port {url}: {e}")