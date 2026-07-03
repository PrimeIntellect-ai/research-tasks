# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import subprocess

def test_nginx_config_fixed():
    nginx_conf_path = "/home/user/config/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Nginx config {nginx_conf_path} does not exist"

    with open(nginx_conf_path, "r") as f:
        content = f.read()

    assert "server unix:/home/user/run/wrong_app.sock;" not in content, "Nginx config still contains the wrong socket path"
    assert "server unix:/home/user/run/app.sock;" in content, "Nginx config does not contain the correct socket path"

def test_hook_fixed():
    hook_path = "/home/user/staging.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} does not exist"

    with open(hook_path, "r") as f:
        content = f.read()

    # The gunicorn command should now be prefixed or exported with TZ=UTC and LANG=en_US.UTF-8
    assert "TZ=UTC" in content, "Hook is missing TZ=UTC environment variable"
    assert "LANG=en_US.UTF-8" in content, "Hook is missing LANG=en_US.UTF-8 environment variable"
    assert "gunicorn" in content, "Hook is missing gunicorn command"

def test_service_health():
    url = "http://127.0.0.1:8080/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.getcode() == 200, f"Expected HTTP 200, got {response.getcode()}"
            data = json.loads(response.read().decode())
            assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to {url}: {e}"
    except json.JSONDecodeError:
        assert False, "Failed to decode JSON response from health endpoint"

def test_processes_running():
    # Check if nginx is running
    try:
        subprocess.check_output(["pgrep", "-f", "nginx"])
    except subprocess.CalledProcessError:
        assert False, "Nginx is not running"

    # Check if gunicorn is running
    try:
        subprocess.check_output(["pgrep", "-f", "gunicorn"])
    except subprocess.CalledProcessError:
        assert False, "Gunicorn is not running"