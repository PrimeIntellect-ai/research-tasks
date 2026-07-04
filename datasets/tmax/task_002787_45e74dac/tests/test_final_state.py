# test_final_state.py
import os
import json
import urllib.request
import urllib.error

def test_success_log_content():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
        assert data.get("status") == "online", "success.log does not contain the correct status."
        assert data.get("version") == "1.0.3", "success.log does not contain the correct version."
    except json.JSONDecodeError:
        assert False, "success.log does not contain valid JSON."

def test_symlink_exists():
    link_path = "/home/user/deploy/current/mnt"
    assert os.path.islink(link_path), f"{link_path} is not a symbolic link."

    target = os.readlink(link_path)
    # The symlink could be absolute or relative
    target_abs = os.path.abspath(os.path.join(os.path.dirname(link_path), target))
    assert target_abs == "/home/user/storage", f"Symlink {link_path} does not point to /home/user/storage."

def test_nginx_config_fixed():
    config_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config missing at {config_path}."

    with open(config_path, "r") as f:
        content = f.read()

    assert "127.0.0.1:9000" in content, "Nginx config was not updated to proxy to port 9000."
    assert "127.0.0.1:9001" not in content, "Nginx config still contains the incorrect port 9001."

def test_python_backend_deployed_and_fixed():
    server_path = "/home/user/deploy/current/server.py"
    assert os.path.isfile(server_path), f"Backend not deployed to {server_path}."

    with open(server_path, "r") as f:
        content = f.read()

    assert "PORT = 9000" in content or "9000" in content, "Deployed Python backend does not seem to bind to port 9000."

def test_live_nginx_request():
    url = "http://127.0.0.1:8080/api/status"
    try:
        req = urllib.request.urlopen(url, timeout=2)
        assert req.getcode() == 200, f"Expected HTTP 200, got {req.getcode()}"

        body = req.read().decode("utf-8")
        data = json.loads(body)
        assert data.get("status") == "online", "Live API did not return the correct status."
    except urllib.error.HTTPError as e:
        assert False, f"HTTP request failed with status code {e.code}. Is the backend running and Nginx reloaded?"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx: {e.reason}"
    except Exception as e:
        assert False, f"Unexpected error making request to Nginx: {e}"