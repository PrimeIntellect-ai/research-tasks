# test_final_state.py
import os
import glob
import urllib.request
import ssl
import time

def test_directories_exist():
    expected_dirs = [
        "/home/user/deployments",
        "/home/user/certs",
        "/home/user/logs"
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Required directory {d} is missing"

def test_tls_certs_exist():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"
    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing"
    assert os.path.isfile(key_path), f"Key file {key_path} is missing"

def test_deploy_script():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing"
    assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable"

def test_symlink_and_content():
    symlink_path = "/home/user/www-current"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"

    target = os.readlink(symlink_path)
    assert target.startswith("/home/user/deployments/"), f"Symlink {symlink_path} does not point to a deployment directory"

    index_path = os.path.join(symlink_path, "index.html")
    assert os.path.isfile(index_path), f"index.html not found in {symlink_path}"

def test_server_running_and_serving():
    url = "https://127.0.0.1:8443/index.html"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Server returned status {response.status}"
            content = response.read().decode('utf-8')
            assert "Deployment Successful" in content, "Server is not serving the correct index.html content"
    except Exception as e:
        assert False, f"Failed to connect to the server at {url}: {e}"

def test_logrotate_files():
    conf_path = "/home/user/logrotate.conf"
    state_path = "/home/user/logrotate.state"

    assert os.path.isfile(conf_path), f"logrotate configuration {conf_path} is missing"
    assert os.path.isfile(state_path), f"logrotate state file {state_path} is missing"

    rotated_logs = glob.glob("/home/user/logs/server.log.*")
    assert len(rotated_logs) > 0, "No rotated log files found in /home/user/logs/"