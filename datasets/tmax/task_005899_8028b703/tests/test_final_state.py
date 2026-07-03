# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest
import subprocess
import time

def test_backup_exists_and_correct():
    backup_path = "/home/user/backup/nginx.conf.bak"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

    with open(backup_path, 'r') as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:9001;" in content, "Backup file does not contain the original proxy_pass directive (9001)."

def test_nginx_config_fixed():
    nginx_conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Nginx config {nginx_conf_path} does not exist."

    with open(nginx_conf_path, 'r') as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:9000;" in content, "Nginx config was not updated to proxy_pass to port 9000."

def test_compiled_backend_exists():
    binary_path = "/home/user/backend/server"
    assert os.path.isfile(binary_path), f"Compiled backend binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Compiled backend binary {binary_path} is not executable."

def test_expect_script_exists():
    expect_script_path = "/home/user/backend/start.exp"
    assert os.path.isfile(expect_script_path), f"Expect script {expect_script_path} does not exist."

def test_result_log_content():
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"Result log {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    assert content == "Backend OK!\n", f"Result log content is incorrect. Expected 'Backend OK!\\n', got {repr(content)}"

def test_nginx_process_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
        assert "nginx" in output and "-p /home/user/nginx" in output, "Nginx is not running with the correct prefix."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check running processes.")

def test_backend_process_running_on_port_9000():
    try:
        # Check if port 9000 is listening
        output = subprocess.check_output(["ss", "-tlnp"]).decode("utf-8")
        assert ":9000" in output, "No process is listening on port 9000."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check listening ports.")