# test_final_state.py

import os
import urllib.request
import json
import pytest

def test_nginx_conf_fixed():
    conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:9000;" in content, "nginx.conf does not contain the corrected proxy_pass to port 9000"

def test_health_log_content():
    log_path = "/home/user/health.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did you run monitor.py?"
    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = 'HEALTHY: {"status": "healthy", "service": "backend"}'
    assert content == expected_content, f"health.log content is incorrect. Expected '{expected_content}', got '{content}'"

def test_monitor_script_exists():
    script_path = "/home/user/monitor.py"
    assert os.path.isfile(script_path), f"File {script_path} is missing"

def test_services_running_and_responding():
    # Test if Nginx is properly proxying to the backend
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to connect to http://127.0.0.1:8080/ - {e}")

    assert status == 200, f"Expected status code 200, got {status}. Is ENV_MODE=production set?"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail("Response body is not valid JSON")

    assert data.get("status") == "healthy", "JSON response does not contain expected status"
    assert data.get("service") == "backend", "JSON response does not contain expected service"