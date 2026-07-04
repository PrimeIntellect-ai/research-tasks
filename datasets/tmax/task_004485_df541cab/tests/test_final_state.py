# test_final_state.py

import os
import json
import pytest

def test_venv_exists():
    path = "/home/user/ci_pipeline/venv/bin/python"
    assert os.path.isfile(path) or os.path.isfile("/home/user/ci_pipeline/venv/bin/python3"), f"Virtual environment python executable not found at {path}"

def test_automate_setup_exists():
    path = "/home/user/ci_pipeline/automate_setup.py"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, 'r') as f:
        content = f.read()
    assert "pexpect" in content, f"File {path} does not appear to use pexpect."

def test_run_pipeline_exists_and_executable():
    path = "/home/user/ci_pipeline/run_pipeline.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_config_json_correct():
    path = "/home/user/legacy_service/config.json"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert config.get("user") == "ci_admin", "Config user is incorrect."
    assert config.get("pass") == "ci_supersecret", "Config pass is incorrect."
    assert str(config.get("port")) == "8080", "Config port is incorrect."
    assert config.get("token") == "TOKEN_842X", "Config token is incorrect."

def test_daemon_running():
    pid_file = "/home/user/ci_pipeline/service.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."
    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid PID."

    # Check if process is running
    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

def test_health_check_log():
    path = "/home/user/ci_pipeline/health_check.log"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, 'r') as f:
        content = f.read().strip()

    expected = '{"status": "ok", "service": "legacy", "token": "TOKEN_842X"}'

    # Try parsing as JSON to allow for formatting differences, or exact match if preferred
    try:
        log_json = json.loads(content)
        expected_json = json.loads(expected)
        assert log_json == expected_json, f"Health check log content does not match expected JSON. Got: {content}"
    except json.JSONDecodeError:
        assert content == expected, f"Health check log content does not match exactly. Got: {content}"