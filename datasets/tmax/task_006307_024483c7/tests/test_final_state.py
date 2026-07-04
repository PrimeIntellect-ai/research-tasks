# test_final_state.py

import os
import tarfile
import pytest

def test_nginx_conf_fixed():
    nginx_conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"File missing: {nginx_conf_path}"
    with open(nginx_conf_path, "r") as f:
        content = f.read()
    assert "proxy_pass http://unix:/home/user/app.sock;" in content, "Nginx config not updated to point to correct socket."

def test_bgp_enabled_log():
    log_path = "/home/user/bgp_enabled.log"
    assert os.path.isfile(log_path), "Router CLI automation failed: bgp_enabled.log not created."
    with open(log_path, "r") as f:
        content = f.read()
    assert "BGP is UP" in content, "bgp_enabled.log does not contain the expected text."

def test_supervisor_running():
    pid_path = "/home/user/supervisor.pid"
    assert os.path.isfile(pid_path), "Supervisor PID file not found."
    with open(pid_path, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file contains invalid PID: {pid_str}"
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Supervisor process with PID {pid} is not running.")

def test_app_sock_exists():
    sock_path = "/home/user/app.sock"
    assert os.path.exists(sock_path), "Web application socket app.sock not created."

def test_backup_tarball():
    tar_path = "/home/user/backups/nginx_backup.tar.gz"
    assert os.path.isfile(tar_path), f"Backup tarball missing at {tar_path}"

    assert tarfile.is_tarfile(tar_path), "Backup file is not a valid tar archive."

    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()
        # Ensure it contains nginx.conf (could be nested depending on how it was tarred)
        assert any("nginx.conf" in name for name in names), "Backup tarball does not contain nginx.conf."

def test_curl_result():
    curl_log_path = "/home/user/curl_result.log"
    assert os.path.isfile(curl_log_path), "curl_result.log was not created."
    with open(curl_log_path, "r") as f:
        content = f.read()
    assert "Hello World!" in content, "curl_result.log does not contain the successful web app response."