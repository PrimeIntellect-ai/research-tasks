# test_final_state.py

import os
import re
import subprocess
import pytest

def test_nginx_config_fixed():
    nginx_conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Missing Nginx config: {nginx_conf_path}"

    with open(nginx_conf_path, "r") as f:
        content = f.read()

    # Check that the proxy_pass port has been updated to 8081
    assert "proxy_pass http://127.0.0.1:8081;" in content or "proxy_pass http://localhost:8081;" in content, \
        "Nginx config does not have the corrected proxy_pass port 8081."

def test_expect_script_exists():
    expect_script_path = "/home/user/start_backend.exp"
    assert os.path.isfile(expect_script_path), f"Missing expect script: {expect_script_path}"

def test_supervisor_script_exists():
    supervisor_script_path = "/home/user/supervisor.sh"
    assert os.path.isfile(supervisor_script_path), f"Missing supervisor script: {supervisor_script_path}"

def test_verification_log_content():
    log_path = "/home/user/verification.log"
    assert os.path.isfile(log_path), f"Missing verification log: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    occurrences = content.count("OK_BACKEND_ACTIVE")
    assert occurrences >= 5, f"Expected at least 5 occurrences of 'OK_BACKEND_ACTIVE' in {log_path}, found {occurrences}."

def test_nginx_listening():
    # Check if port 8080 is listening
    try:
        output = subprocess.check_output(["ss", "-tln"], text=True)
        assert ":8080 " in output, "Nginx does not appear to be listening on port 8080."
    except FileNotFoundError:
        # Fallback if ss is not available
        pass

def test_socat_listening():
    # Check if port 9000 is listening (socat)
    try:
        output = subprocess.check_output(["ss", "-tln"], text=True)
        assert ":9000 " in output, "socat does not appear to be listening on port 9000."
    except FileNotFoundError:
        pass

def test_socat_process_running():
    try:
        output = subprocess.check_output(["ps", "aux"], text=True)
        assert "socat" in output, "socat process is not running."
    except Exception:
        pass