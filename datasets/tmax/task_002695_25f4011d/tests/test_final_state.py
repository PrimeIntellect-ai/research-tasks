# test_final_state.py

import os
import json
import subprocess
import urllib.request
import urllib.error
import pytest

def test_service_running():
    """Verify supervisord and monitor.py are running."""
    # Check supervisord
    try:
        output = subprocess.check_output(["pgrep", "-f", "supervisord"], text=True)
        assert output.strip(), "supervisord is not running"
    except subprocess.CalledProcessError:
        pytest.fail("supervisord is not running")

    # Check monitor.py
    try:
        output = subprocess.check_output(["pgrep", "-f", "monitor.py"], text=True)
        assert output.strip(), "monitor.py is not running"
    except subprocess.CalledProcessError:
        pytest.fail("monitor.py is not running")

def test_idempotency():
    """Verify deploy_monitor.sh is idempotent by running it again."""
    script_path = "/home/user/deploy_monitor.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy_monitor.sh failed on second run. Output: {result.stderr}"

def test_users_json_content():
    """Verify users.json contains the expected configuration."""
    users_file = "/home/user/config/users.json"
    assert os.path.exists(users_file), f"{users_file} does not exist"

    with open(users_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{users_file} is not valid JSON")

    expected = {"groups": {"admin": ["alice"], "monitors": ["bob", "charlie"]}}
    assert data == expected, f"Content of {users_file} does not match expected structure"

def test_health_endpoint():
    """Verify /health endpoint returns correct JSON."""
    url = "http://127.0.0.1:8443/health"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        assert req.getcode() == 200, f"/health returned status {req.getcode()}"
        data = json.loads(req.read().decode("utf-8"))
    except Exception as e:
        pytest.fail(f"Failed to access /health endpoint: {e}")

    expected = {"status": "ok", "timezone": "America/St_Johns", "locale": "fr_CA.UTF-8"}
    assert data == expected, f"/health endpoint returned unexpected data: {data}"

def test_users_endpoint():
    """Verify /users endpoint returns correct JSON."""
    url = "http://127.0.0.1:8443/users"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        assert req.getcode() == 200, f"/users returned status {req.getcode()}"
        data = json.loads(req.read().decode("utf-8"))
    except Exception as e:
        pytest.fail(f"Failed to access /users endpoint: {e}")

    expected = {"groups": {"admin": ["alice"], "monitors": ["bob", "charlie"]}}
    assert data == expected, f"/users endpoint returned unexpected data: {data}"

def test_health_result_log():
    """Verify health_result.log contains the /health response."""
    log_file = "/home/user/health_result.log"
    assert os.path.exists(log_file), f"{log_file} does not exist"

    with open(log_file, "r") as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"{log_file} does not contain valid JSON")

    expected = {"status": "ok", "timezone": "America/St_Johns", "locale": "fr_CA.UTF-8"}
    assert data == expected, f"Content of {log_file} does not match expected structure"

def test_supervisor_config():
    """Verify supervisord.conf contains autorestart and environment variables."""
    conf_file = "/home/user/supervisord.conf"
    assert os.path.exists(conf_file), f"{conf_file} does not exist"

    with open(conf_file, "r") as f:
        content = f.read().lower()

    assert "autorestart" in content, "autorestart policy not found in supervisord.conf"

    # Check for environment variables, allowing for different spacing and quoting
    assert "environment" in content, "environment variables not found in supervisord.conf"
    assert "america/st_johns" in content, "TZ environment variable not set correctly in supervisord.conf"
    assert "fr_ca.utf-8" in content, "LANG environment variable not set correctly in supervisord.conf"