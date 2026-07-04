# test_final_state.py

import os
import urllib.request
import ssl
import pytest

def test_symlink_fixed():
    path = "/home/user/app/current"
    assert os.path.islink(path), f"{path} is not a symlink"
    target = os.readlink(path)
    # The absolute path or relative path could be used, but realpath should resolve to /home/user/app/releases/v1
    assert os.path.realpath(path) == "/home/user/app/releases/v1", f"Symlink {path} does not resolve to /home/user/app/releases/v1"

def test_nginx_conf_proxy_pass():
    path = "/home/user/nginx.conf"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:8080;" in content, "nginx.conf does not contain 'proxy_pass http://127.0.0.1:8080;'"

def test_nginx_conf_ssl():
    path = "/home/user/nginx.conf"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    assert "ssl_certificate /home/user/cert.pem;" in content, "nginx.conf missing 'ssl_certificate /home/user/cert.pem;'"
    assert "ssl_certificate_key /home/user/key.pem;" in content, "nginx.conf missing 'ssl_certificate_key /home/user/key.pem;'"

def test_ssl_certificates_exist():
    assert os.path.isfile("/home/user/cert.pem"), "/home/user/cert.pem does not exist"
    assert os.path.isfile("/home/user/key.pem"), "/home/user/key.pem does not exist"

def test_nginx_running():
    pid_file = "/home/user/nginx.pid"
    assert os.path.isfile(pid_file), f"Nginx PID file {pid_file} does not exist. Nginx might not be running."
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid PID"
    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Nginx process with PID {pid} is not running")

def test_health_monitor_script_exists():
    path = "/home/user/health_monitor.py"
    assert os.path.isfile(path), f"File {path} does not exist"

def test_health_log_content():
    path = "/home/user/health.log"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    assert "STATUS: UP" in content, f"{path} does not contain 'STATUS: UP'"

def test_services_actually_working():
    # Verify that Nginx is actually proxying to the backend successfully
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://127.0.0.1:8443/")
        with urllib.request.urlopen(req, context=ctx, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200 from Nginx, got {response.status}"
            body = response.read().decode('utf-8')
            assert '{"status": "ok"}' in body, "Response body does not match expected backend output"
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx on port 8443 or backend is not responding properly: {e}")