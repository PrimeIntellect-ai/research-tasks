# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def test_config_json_updated():
    config_path = "/home/user/app/config.json"
    assert os.path.isfile(config_path), f"Configuration file {config_path} does not exist."

    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {config_path} is not valid JSON.")

    assert config.get("original_key") == "do_not_delete", "The original key 'original_key' was removed or altered."
    assert config.get("proxy_active") is True, "The key 'proxy_active' is not set to true."
    assert config.get("backend_port") == 8081, "The key 'backend_port' is not set to 8081."

def test_configure_script_exists():
    script_path = "/home/user/configure.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_proxy_script_exists():
    script_path = "/home/user/proxy.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_proxy_test_log():
    log_path = "/home/user/proxy_test.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {log_path} is not valid JSON: {content}")

    assert data.get("status") == "ok", "Expected status 'ok' in response."
    assert data.get("message") == "Backend operational", "Expected message 'Backend operational' in response."
    assert data.get("config_loaded") is True, "Expected config_loaded to be true in response."

def test_backend_running():
    try:
        req = urllib.request.Request("http://localhost:8081/")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Backend returned status {response.status}"
            data = json.loads(response.read().decode())
            assert data.get("status") == "ok", "Backend response JSON missing 'status': 'ok'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to backend on port 8081: {e}")

def test_proxy_running():
    try:
        req = urllib.request.Request("http://localhost:8000/")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Proxy returned status {response.status}"
            data = json.loads(response.read().decode())
            assert data.get("status") == "ok", "Proxy response JSON missing 'status': 'ok'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy on port 8000: {e}")