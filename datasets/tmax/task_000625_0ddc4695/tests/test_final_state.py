# test_final_state.py

import os
import subprocess
import requests
import configparser
import pytest

def test_app_data_size():
    app_data_dir = "/home/user/app_data"
    assert os.path.isdir(app_data_dir), f"Directory missing: {app_data_dir}"

    total_size = 0
    for dirpath, _, filenames in os.walk(app_data_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    size_mb = total_size / (1024 * 1024)
    assert size_mb < 5.0, f"Total size of {app_data_dir} is {size_mb:.2f}MB, which is not strictly less than 5MB. The junk file may not have been removed."

def test_supervisord_conf():
    conf_path = "/home/user/supervisor/supervisord.conf"
    assert os.path.isfile(conf_path), f"Missing configuration file: {conf_path}"

    config = configparser.ConfigParser()
    # supervisord.conf might have duplicate sections or other quirks, but standard configparser usually handles basic ones.
    # To be safe against parsing errors from includes, we read it directly.
    config.read(conf_path)

    assert "program:api-service" in config.sections(), "Missing [program:api-service] section in supervisord.conf"

    autorestart = config.get("program:api-service", "autorestart", fallback="").lower()
    assert autorestart == "true", f"Expected autorestart=true in [program:api-service], got '{autorestart}'"

    startretries = config.get("program:api-service", "startretries", fallback="")
    assert startretries == "5", f"Expected startretries=5 in [program:api-service], got '{startretries}'"

def test_supervisor_status():
    result = subprocess.run(
        ["supervisorctl", "-c", "/home/user/supervisor/supervisord.conf", "status", "api-service"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"supervisorctl command failed: {result.stderr}"
    assert "RUNNING" in result.stdout, f"api-service is not RUNNING. Output: {result.stdout}"

def test_nginx_ping():
    try:
        response = requests.get("http://127.0.0.1:8080/ping", timeout=5)
        assert response.status_code == 200, f"Expected HTTP 200 OK for /ping, got {response.status_code}. Response: {response.text}"
        assert response.text.strip() == "pong", f"Expected response body 'pong', got '{response.text}'"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 for /ping: {e}")

def test_nginx_data_post():
    try:
        response = requests.post("http://127.0.0.1:8080/data", timeout=5)
        assert response.status_code == 200, f"Expected HTTP 200 OK for POST /data, got {response.status_code}. Response: {response.text}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 for POST /data: {e}")