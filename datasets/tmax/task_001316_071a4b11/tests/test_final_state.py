# test_final_state.py

import os
import stat
import subprocess
import pytest
import urllib.request

def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def test_automate_exp_exists_and_executable():
    path = "/home/user/automate.exp"
    assert is_executable(path), f"{path} must exist and be executable."
    with open(path, 'r') as f:
        content = f.read()
    assert 'expect' in content, f"{path} should be an expect script."
    assert 'prod' in content, f"{path} missing 'prod' answer."
    assert '8181' in content, f"{path} missing '8181' answer."
    assert 'y' in content, f"{path} missing 'y' answer."

def test_deploy_sh_exists_and_executable():
    path = "/home/user/deploy.sh"
    assert is_executable(path), f"{path} must exist and be executable."

def test_health_monitor_sh_exists_and_executable():
    path = "/home/user/health_monitor.sh"
    assert is_executable(path), f"{path} must exist and be executable."

def test_service_conf_content():
    path = "/home/user/legacy_app/service.conf"
    assert os.path.isfile(path), f"{path} does not exist. Was deploy.sh run?"
    with open(path, 'r') as f:
        content = f.read()
    assert "ENV=prod" in content, f"{path} missing ENV=prod"
    assert "PORT=8181" in content, f"{path} missing PORT=8181"
    assert "VERBOSE=y" in content, f"{path} missing VERBOSE=y"

def test_health_report_log():
    path = "/home/user/health_report.log"
    assert os.path.isfile(path), f"{path} does not exist. Was health_monitor.sh run?"
    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    assert len(lines) >= 1, f"{path} is empty."
    assert "STATUS: HEALTHY" in lines[-1], f"{path} should contain STATUS: HEALTHY"

def test_deploy_sh_idempotency():
    # Since service.conf should already exist, running deploy.sh again should output the specific string
    result = subprocess.run(["/home/user/deploy.sh"], capture_output=True, text=True)
    assert result.returncode == 0, "/home/user/deploy.sh did not exit with status code 0."
    assert "Deployment already configured." in result.stdout, "deploy.sh did not output the expected message when already deployed."

def test_service_running():
    try:
        response = urllib.request.urlopen("http://127.0.0.1:8181/health", timeout=2)
        body = response.read().decode('utf-8')
        assert body == "OK", "Health endpoint did not return 'OK'."
    except Exception as e:
        pytest.fail(f"Could not connect to the service on port 8181: {e}")