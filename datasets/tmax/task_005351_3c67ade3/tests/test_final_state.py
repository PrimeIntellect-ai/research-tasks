# test_final_state.py
import os
import re
import stat
import smtplib
import requests
import time
import pytest

def test_bash_profile_exported_port():
    profile_path = "/home/user/.bash_profile"
    assert os.path.exists(profile_path), f"File {profile_path} does not exist."
    with open(profile_path, "r") as f:
        content = f.read()
    # allow export BACKEND_PORT=8025 or export BACKEND_PORT="8025" or export BACKEND_PORT='8025'
    assert re.search(r'^export\s+BACKEND_PORT=[\'"]?8025[\'"]?(?:\s|$)', content, re.MULTILINE), \
        f"Could not find 'export BACKEND_PORT=8025' in {profile_path}"

def test_start_services_script_executable():
    script_path = "/home/user/start_services.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_pid_files_exist():
    run_dir = "/home/user/run"
    assert os.path.isdir(run_dir), f"Directory {run_dir} does not exist."

    for pid_file in ["backend.pid", "proxy.pid", "health.pid"]:
        pid_path = os.path.join(run_dir, pid_file)
        assert os.path.exists(pid_path), f"PID file {pid_path} does not exist."
        with open(pid_path, "r") as f:
            pid = f.read().strip()
            assert pid.isdigit(), f"PID file {pid_path} does not contain a valid numeric PID."

def test_health_check_endpoint():
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to health check endpoint on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Health check response is not valid JSON: {response.text}")

    assert data.get("status") == "healthy", f"Expected status 'healthy', got '{data.get('status')}'"
    assert str(data.get("backend_port")) == "8025", f"Expected backend_port 8025, got '{data.get('backend_port')}'"

def test_smtp_proxy_and_backend():
    try:
        # Connect to proxy port 2525
        server = smtplib.SMTP("127.0.0.1", 2525, timeout=5)
        server.ehlo("verifier.local")
        server.sendmail("test@verifier.com", ["admin@local"], "Subject: test msg\r\n\r\nHello World")
        server.quit()
    except Exception as e:
        pytest.fail(f"SMTP interaction failed on port 2525: {e}")

    # allow some time for backend to write to file
    time.sleep(1)

    log_path = "/home/user/mail_sink.log"
    assert os.path.exists(log_path), f"Mail sink log {log_path} does not exist."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "test@verifier.com" in log_content, "Sender 'test@verifier.com' not found in mail_sink.log"
    assert "admin@local" in log_content, "Recipient 'admin@local' not found in mail_sink.log"
    assert "Hello World" in log_content, "Message body 'Hello World' not found in mail_sink.log"