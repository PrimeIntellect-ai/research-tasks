# test_final_state.py

import os
import json
import urllib.request
import urllib.error

def test_dummy_file():
    path = "/home/user/workspace/data/dummy.dat"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.getsize(path) == 5242880, f"File {path} must be exactly 5242880 bytes."

def test_config_file():
    path = "/home/user/workspace/config/settings.json"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} is not valid JSON."

    assert data.get("monitor_dir") == "/home/user/workspace/data", "monitor_dir key is incorrect."
    assert data.get("quota_mb") == 15, "quota_mb key is incorrect."

def test_go_binary():
    path = "/home/user/workspace/disk_monitor/monitor_service"
    assert os.path.isfile(path), f"Go binary {path} does not exist."
    assert os.access(path, os.X_OK), f"Go binary {path} is not executable."

def test_http_service():
    url = "http://127.0.0.1:8080/status"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                assert False, "Service did not return valid JSON."

            assert data.get("status") == "ok", "Expected status to be 'ok'."
            assert data.get("usage_mb") == 5, f"Expected usage_mb to be 5, got {data.get('usage_mb')}."
            assert data.get("quota_mb") == 15, f"Expected quota_mb to be 15, got {data.get('quota_mb')}."
    except urllib.error.URLError as e:
        assert False, f"Could not connect to service on port 8080: {e}"

def test_bash_script_and_log():
    script_path = "/home/user/workspace/check_conn.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."

    log_path = "/home/user/workspace/monitor_results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            assert False, f"Log file {log_path} does not contain valid JSON."

        assert data.get("status") == "ok", "Log JSON status is incorrect."
        assert data.get("usage_mb") == 5, "Log JSON usage_mb is incorrect."
        assert data.get("quota_mb") == 15, "Log JSON quota_mb is incorrect."