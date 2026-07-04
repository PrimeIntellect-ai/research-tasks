# test_final_state.py

import os
import subprocess
import pytest

APP_DIR = "/home/user/app"
CONFIG_FILE = os.path.join(APP_DIR, "config.env")
SERVER_BIN = os.path.join(APP_DIR, "server")
CLIENT_BIN = os.path.join(APP_DIR, "client")
MONITOR_SCRIPT = os.path.join(APP_DIR, "monitor.sh")
SERVER_LOG = os.path.join(APP_DIR, "server.log")
ROTATED_LOG = os.path.join(APP_DIR, "archive/server_rotated.log")
HEALTH_LOG = os.path.join(APP_DIR, "health.log")

def test_config_env():
    assert os.path.isfile(CONFIG_FILE), f"{CONFIG_FILE} is missing."
    with open(CONFIG_FILE, "r") as f:
        content = f.read()
    assert "CLIENT_TARGET_IP=127.0.0.2" in content, "CLIENT_TARGET_IP is not correctly set to 127.0.0.2 in config.env"
    assert "CLIENT_PORT=8888" in content, "CLIENT_PORT is not correctly set to 8888 in config.env"
    assert "SERVER_BIND_IP=127.0.0.2" in content, "SERVER_BIND_IP should remain 127.0.0.2"
    assert "SERVER_PORT=8888" in content, "SERVER_PORT should remain 8888"

def test_binaries_compiled():
    assert os.path.isfile(SERVER_BIN), f"Server binary {SERVER_BIN} is missing. Did you compile it?"
    assert os.access(SERVER_BIN, os.X_OK), f"Server binary {SERVER_BIN} is not executable."

    assert os.path.isfile(CLIENT_BIN), f"Client binary {CLIENT_BIN} is missing. Did you compile it?"
    assert os.access(CLIENT_BIN, os.X_OK), f"Client binary {CLIENT_BIN} is not executable."

def test_server_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "./server"]).decode()
        assert output.strip(), "Server process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("Server process is not running. pgrep did not find it.")

def test_monitor_script_exists_and_executable():
    assert os.path.isfile(MONITOR_SCRIPT), f"Monitor script {MONITOR_SCRIPT} is missing."
    assert os.access(MONITOR_SCRIPT, os.X_OK), f"Monitor script {MONITOR_SCRIPT} is not executable."

def test_rotated_log():
    assert os.path.isfile(ROTATED_LOG), f"Rotated log {ROTATED_LOG} is missing. Did the monitor script run?"
    with open(ROTATED_LOG, "r") as f:
        content = f.read()
    assert "Server started on 127.0.0.2:8888" in content, f"Expected startup message not found in {ROTATED_LOG}."

def test_server_log_truncated_and_appended():
    assert os.path.isfile(SERVER_LOG), f"Server log {SERVER_LOG} is missing."
    with open(SERVER_LOG, "r") as f:
        content = f.read()
    assert "Health check received." in content, f"Expected health check message not found in {SERVER_LOG}."
    assert "Server started on" not in content, f"Original startup message should have been truncated from {SERVER_LOG}."

def test_health_log():
    assert os.path.isfile(HEALTH_LOG), f"Health log {HEALTH_LOG} is missing."
    with open(HEALTH_LOG, "r") as f:
        content = f.read()
    assert "HEALTH_OK" in content, f"Expected 'HEALTH_OK' not found in {HEALTH_LOG}."