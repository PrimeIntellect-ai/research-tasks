# test_final_state.py

import os
import urllib.request
import json
import time

def test_app_conf_exists_and_correct():
    conf_path = "/home/user/app.conf"
    assert os.path.exists(conf_path), f"{conf_path} does not exist. The config_wizard.py was likely not run correctly."

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "ENV=production" in content, "app.conf does not contain the correct ENV value."
    assert "PORT=8123" in content, "app.conf does not contain the correct PORT value."

def test_server_running_and_serving_status():
    url = "http://localhost:8123/status"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Server returned status {response.status} instead of 200."
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("status") == "ok", "Server response JSON does not contain 'status': 'ok'."
            assert data.get("environment") == "production", "Server response JSON does not contain 'environment': 'production'."
    except urllib.error.URLError as e:
        assert False, f"Could not connect to the server on port 8123: {e}. Is the server running in the background?"

def test_deployment_status_log():
    log_path = "/home/user/deployment_status.log"
    assert os.path.exists(log_path), f"{log_path} does not exist. Did monitor.py create it?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_log = "[HEALTHY] Service running on port 8123 in production mode"
    assert expected_log in content, f"Log content does not match the expected string. Found: {content}"

def test_student_scripts_exist():
    deploy_script = "/home/user/deploy_pipeline.py"
    monitor_script = "/home/user/monitor.py"

    assert os.path.exists(deploy_script), f"{deploy_script} does not exist."
    assert os.path.exists(monitor_script), f"{monitor_script} does not exist."