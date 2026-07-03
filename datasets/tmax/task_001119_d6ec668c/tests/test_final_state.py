# test_final_state.py

import os
import subprocess
import pytest
import stat

def test_certs_exist():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"
    assert os.path.exists(cert_path), f"Missing certificate file: {cert_path}"
    assert os.path.exists(key_path), f"Missing key file: {key_path}"

def test_logs_dir_exists():
    logs_dir = "/home/user/logs"
    assert os.path.exists(logs_dir), f"Missing logs directory: {logs_dir}"
    assert os.path.isdir(logs_dir), f"{logs_dir} is not a directory"

def test_webhook_service_fixed():
    path = "/home/user/webhook_service.py"
    assert os.path.exists(path), f"Missing required file: {path}"

    with open(path, 'r') as f:
        content = f.read()

    assert "RotatingFileHandler" in content, "webhook_service.py does not use RotatingFileHandler"
    assert "maxBytes=1024" in content.replace(" ", ""), "webhook_service.py does not configure maxBytes=1024"
    assert "backupCount=3" in content.replace(" ", ""), "webhook_service.py does not configure backupCount=3"
    assert "ssl." in content, "webhook_service.py does not contain TLS configuration"
    assert "cert.pem" in content, "webhook_service.py does not reference cert.pem"
    assert "key.pem" in content, "webhook_service.py does not reference key.pem"

def test_ci_pipeline_script():
    script_path = "/home/user/ci_pipeline.sh"
    assert os.path.exists(script_path), f"Missing CI pipeline script: {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

    with open(script_path, 'r') as f:
        content = f.read()

    assert "CI SUCCESS" in content, f"{script_path} does not contain 'CI SUCCESS'"
    assert "curl" in content, f"{script_path} does not use curl"
    assert "8443" in content, f"{script_path} does not reference port 8443"

def test_ci_pipeline_execution():
    script_path = "/home/user/ci_pipeline.sh"
    assert os.path.exists(script_path), "Script missing, cannot run execution test"

    try:
        result = subprocess.run([script_path], capture_output=True, text=True, timeout=15)
        assert result.returncode == 0, f"CI pipeline script failed with exit code {result.returncode}. Stderr: {result.stderr}"
        assert "CI SUCCESS" in result.stdout, "CI pipeline script did not output 'CI SUCCESS'"
    except subprocess.TimeoutExpired:
        pytest.fail("CI pipeline script timed out. Ensure the background process is terminated correctly.")