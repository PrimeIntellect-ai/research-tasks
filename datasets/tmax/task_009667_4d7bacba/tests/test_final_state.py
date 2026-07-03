# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error

def test_backup_nginx_config():
    backup_path = "/home/user/backup/nginx.conf.bak"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist"
    with open(backup_path, 'r') as f:
        content = f.read()
    assert "wrong_health_path.sock" in content, "Backup file does not contain the original wrong socket path"

def test_fixed_nginx_config():
    config_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config {config_path} does not exist"
    with open(config_path, 'r') as f:
        content = f.read()
    assert "proxy_pass http://unix:/home/user/app/health.sock;" in content, "Nginx config does not contain the correct socket path"

def test_health_service_compiled_and_running():
    bin_path = "/home/user/app/health_service"
    assert os.path.isfile(bin_path), f"Compiled executable {bin_path} does not exist"
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable"

    # Check if process is running
    try:
        output = subprocess.check_output(["pgrep", "-f", "health_service"]).decode("utf-8")
        assert output.strip(), "health_service is not running"
    except subprocess.CalledProcessError:
        assert False, "health_service is not running"

def test_nginx_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "nginx"]).decode("utf-8")
        assert output.strip(), "nginx is not running"
    except subprocess.CalledProcessError:
        assert False, "nginx is not running"

def test_health_result_log():
    log_path = "/home/user/health_result.log"
    assert os.path.isfile(log_path), f"Result log {log_path} does not exist"
    with open(log_path, 'r') as f:
        content = f.read()
    assert content == "MAIL_HEALTH_OK\n", f"Result log contains incorrect output: {repr(content)}"

def test_health_endpoint_live():
    # Verify the endpoint is actually functional as expected
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=2)
        response = req.read().decode("utf-8")
        assert response == "MAIL_HEALTH_OK\n", "Live health endpoint returned incorrect response"
    except Exception as e:
        assert False, f"Failed to reach health endpoint: {e}"