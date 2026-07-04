# test_final_state.py

import os
import stat
import urllib.request
import pytest

def test_nginx_config_fixed():
    config_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config {config_path} is missing."

    with open(config_path, "r") as f:
        content = f.read()
        assert "proxy_pass http://127.0.0.1:8081" in content or "proxy_pass http://localhost:8081" in content, \
            "Nginx config does not contain the corrected proxy_pass port (8081)."

def test_supervisor_script_exists_and_executable():
    script_path = "/home/user/scripts/supervisor.sh"
    assert os.path.isfile(script_path), f"Supervisor script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Supervisor script {script_path} is not executable."

def test_supervisor_script_contents():
    script_path = "/home/user/scripts/supervisor.sh"
    with open(script_path, "r") as f:
        content = f.read()

    # Check for loop
    assert "while" in content or "until" in content, "Supervisor script does not appear to contain a loop."

    # Check for backend execution
    assert "/home/user/app/backend.sh" in content, "Supervisor script does not execute the backend script."

    # Check for log redirection
    assert "/home/user/logs/backend.log" in content, "Supervisor script does not redirect to the expected log file."

    # Check for log rotation logic (1024 bytes)
    assert "1024" in content, "Supervisor script does not contain the 1024 byte size check."
    assert "backend.log.old" in content, "Supervisor script does not rename to backend.log.old."

    # Check for alerting
    assert "Subject: Backend Crash Alert" in content, "Supervisor script does not contain the required alert subject."
    assert "/home/user/mail/alerts" in content, "Supervisor script does not write to the alerts file."

def test_success_file_contents():
    success_path = "/home/user/success.txt"
    assert os.path.isfile(success_path), f"Success file {success_path} is missing."

    with open(success_path, "r") as f:
        content = f.read()

    assert "Directory listing" in content, "Success file does not contain the expected output from the backend service."