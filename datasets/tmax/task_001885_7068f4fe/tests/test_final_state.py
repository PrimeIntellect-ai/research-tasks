# test_final_state.py

import os
import subprocess
import urllib.request
import json
import pytest

def test_nginx_config_and_running():
    config_path = '/home/user/nginx/nginx.conf'
    assert os.path.exists(config_path), f"{config_path} does not exist"

    with open(config_path, 'r') as f:
        config = f.read()

    assert "proxy_pass http://127.0.0.1:9001;" in config, "Nginx config was not updated to proxy requests to 127.0.0.1:9001"

    proc = subprocess.run(['pgrep', '-f', 'nginx'], capture_output=True, text=True)
    assert proc.returncode == 0, "Nginx process is not running"

def test_backend_running():
    proc = subprocess.run(['pgrep', '-f', 'app.py'], capture_output=True, text=True)
    assert proc.returncode == 0, "The Python backend (app.py) is not running"

def test_expect_script():
    script_path = '/home/user/start_backend.exp'
    assert os.path.exists(script_path), f"{script_path} does not exist"

    with open(script_path, 'r') as f:
        content = f.read()

    assert "8374" in content, "The expect script does not contain the required pin code '8374'"
    assert "Europe/Paris" in content, "The expect script does not set the timezone to 'Europe/Paris'"
    assert "spawn" in content or "app.py" in content, "The expect script does not appear to spawn the backend"

def test_nginx_proxy_response():
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
            assert data.get("timezone") == "Europe/Paris", f"Expected timezone 'Europe/Paris', got {data.get('timezone')}"
    except Exception as e:
        pytest.fail(f"Failed to get a successful response from the Nginx proxy: {e}")

def test_monitor_script():
    monitor_path = '/home/user/monitor.py'
    assert os.path.exists(monitor_path), f"{monitor_path} does not exist"

    with open(monitor_path, 'r') as f:
        content = f.read()

    assert "try" in content and "except" in content, "monitor.py does not appear to handle exceptions gracefully (missing try/except blocks)"

def test_health_log():
    log_path = '/home/user/health.log'
    assert os.path.exists(log_path), f"{log_path} does not exist. Did the monitor script run?"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "SUCCESS" in content, "health.log does not contain the 'SUCCESS' string"