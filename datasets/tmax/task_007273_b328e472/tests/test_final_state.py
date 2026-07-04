# test_final_state.py

import os
import stat
import json
import subprocess
import urllib.request
import urllib.error
import pytest

def test_settings_env_exists_and_content():
    env_path = "/home/user/deploy/settings.env"
    assert os.path.exists(env_path), f"File {env_path} does not exist."
    with open(env_path, "r") as f:
        content = f.read()
    assert "METRICS_OUT_DIR=/home/user/app_data/metrics" in content, "METRICS_OUT_DIR not properly set in settings.env"
    assert "METRICS_PORT=8888" in content, "METRICS_PORT not properly set in settings.env"

def test_disk_monitor_py_exists():
    py_path = "/home/user/deploy/disk_monitor.py"
    assert os.path.exists(py_path), f"File {py_path} does not exist."

def test_job_wrapper_exists_and_executable():
    sh_path = "/home/user/deploy/job_wrapper.sh"
    assert os.path.exists(sh_path), f"File {sh_path} does not exist."
    st = os.stat(sh_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {sh_path} is not executable."

def test_port_forwarding_active():
    url = "http://127.0.0.1:8888/ping"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as response:
            body = response.read().decode("utf-8")
            assert "PONG" in body, f"Expected PONG from port 8888, got {body}"
    except Exception as e:
        pytest.fail(f"Port forwarding on 8888 failed or dummy server unreachable: {e}")

def test_wrapper_execution_and_report():
    sh_path = "/home/user/deploy/job_wrapper.sh"

    # Run the wrapper script with an empty environment
    result = subprocess.run(["env", "-i", "/bin/bash", sh_path], capture_output=True, text=True)
    assert result.returncode == 0, f"job_wrapper.sh failed to execute. stderr: {result.stderr}"

    report_path = "/home/user/app_data/metrics/report.json"
    assert os.path.exists(report_path), f"Report file {report_path} was not created. Did the script write to fallback?"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert data.get("status") == "DISK_OK", "JSON status is not DISK_OK."
    assert data.get("directory") == "/home/user/app_data/metrics", "JSON directory path is incorrect."