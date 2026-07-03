# test_final_state.py

import os
import json
import tarfile
import urllib.request
import ssl
import pytest

def test_scripts_exist():
    bash_script = "/home/user/setup_and_run.sh"
    python_script = "/home/user/monitor.py"

    assert os.path.isfile(bash_script), f"Deployment script {bash_script} is missing."
    assert os.access(bash_script, os.X_OK), f"Deployment script {bash_script} is not executable."
    assert os.path.isfile(python_script), f"Python daemon {python_script} is missing."

def test_certs_exist():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Private key file {key_path} is missing."

def test_backup_created():
    backup_path = "/home/user/backup_dir/data_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} was not created."

    # Verify it is a valid tar.gz and contains the large file
    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            assert any("large_file.dat" in name for name in names), "Backup does not contain the expected data files."
    except tarfile.TarError:
        pytest.fail(f"Backup file {backup_path} is not a valid gzip-compressed tarball.")

def test_alert_logged():
    log_path = "/home/user/alerts.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    expected_alert = "ALERT: data_dir exceeds 50MB"
    assert expected_alert in content, f"Expected alert string not found in {log_path}."

def test_pid_file_and_process_running():
    pid_file = "/home/user/monitor.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid numeric PID."

    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from {pid_file} is not running.")

def test_https_server_response():
    url = "https://127.0.0.1:8443/status"

    # Ignore self-signed certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = response.read().decode('utf-8')

            try:
                json_data = json.loads(data)
            except json.JSONDecodeError:
                pytest.fail("Server response is not valid JSON.")

            assert json_data.get("disk_status") == "ALERT", "Expected 'disk_status' to be 'ALERT'."
            assert json_data.get("backup_path") == "/home/user/backup_dir/data_backup.tar.gz", "Incorrect 'backup_path' in JSON response."

    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the HTTPS server at {url}: {e}")