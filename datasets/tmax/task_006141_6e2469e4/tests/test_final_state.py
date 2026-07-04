# test_final_state.py

import os
import glob
import urllib.request
import urllib.error
import subprocess
import pytest

def test_nginx_running():
    """Check if Nginx is running with the specified configuration."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "nginx.*-c /home/user/nginx.conf"])
        assert output.strip(), "Nginx is not running with the specified config."
    except subprocess.CalledProcessError:
        pytest.fail("Nginx is not running with the specified config.")

def test_backend_servers_running():
    """Check if backend C servers are listening on ports 8081 and 8082."""
    def is_listening(port):
        try:
            subprocess.check_output(["lsof", "-i", f":{port}"])
            return True
        except subprocess.CalledProcessError:
            return False

    assert is_listening(8081), "Backend server is not listening on port 8081."
    assert is_listening(8082), "Backend server is not listening on port 8082."

def test_load_balancer_response():
    """Check if the load balancer returns OK_V2."""
    try:
        req = urllib.request.Request("http://127.0.0.1:8080")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8')
            assert "OK_V2" in body, f"Load balancer did not return OK_V2. Got: {body}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to load balancer on port 8080: {e}")

def test_deploy_test_log():
    """Check if the deploy_test.log contains OK_V2."""
    log_path = "/home/user/deploy_test.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
        assert "OK_V2" in content, "Log file does not contain OK_V2."

def test_backup_presence():
    """Check if backup binaries exist in /home/user/backup/."""
    backup_dir = "/home/user/backup"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist."
    backups = glob.glob(os.path.join(backup_dir, "server_bin_*"))
    assert len(backups) >= 1, "No backup binaries found in /home/user/backup/"

def test_deploy_script_permissions():
    """Check if deploy.sh is executable."""
    script_path = "/home/user/deploy.sh"
    assert os.path.exists(script_path), f"Deployment script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable."