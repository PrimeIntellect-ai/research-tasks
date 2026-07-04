# test_final_state.py

import os
import ssl
import urllib.request
import pytest

def test_certificates_exist():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"
    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Key file {key_path} is missing."

def test_deployment_symlink_and_target():
    symlink_path = "/home/user/webroot/latest"
    target_dir = "/home/user/deployments/app-v1.0"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.path.isdir(target_dir), f"Deployment directory {target_dir} is missing."

    # Check if symlink resolves to the correct directory or if the file exists through it
    index_file = os.path.join(symlink_path, "index.html")
    assert os.path.isfile(index_file), f"index.html not found through symlink at {index_file}."

def test_deploy_log():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "SUCCESS: app-v1.0 deployed" in content, "Log file does not contain the required success message."

def test_server_pid_and_process():
    pid_path = "/home/user/server.pid"
    assert os.path.isfile(pid_path), f"PID file {pid_path} is missing."

    with open(pid_path, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), "PID file does not contain a valid integer."

    # Check if process is running
    try:
        os.kill(int(pid_str), 0)
    except OSError:
        pytest.fail(f"Process with PID {pid_str} is not running.")

def test_https_server_serving_content():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:8443/index.html"
    try:
        response = urllib.request.urlopen(url, context=ctx, timeout=5)
        content = response.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to fetch content from {url}: {e}")

    assert "Hello World!" in content, "The HTTPS server did not serve the expected content."