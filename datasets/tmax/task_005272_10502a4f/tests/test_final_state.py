# test_final_state.py
import os
import re
import subprocess
import requests
import pytest

def test_setup_script_exists_and_executable():
    script_path = "/home/user/setup_gateway.sh"
    assert os.path.isfile(script_path), f"Setup script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Setup script at {script_path} is not executable"

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"logrotate.conf missing at {conf_path}"
    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/logs/access.log" in content, "logrotate.conf does not target /home/user/logs/access.log"
    assert "daily" in content, "logrotate.conf missing 'daily' directive"
    assert re.search(r"rotate\s+3", content), "logrotate.conf missing 'rotate 3' directive"
    assert "compress" in content, "logrotate.conf missing 'compress' directive"

def test_nginx_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode()
        assert "nginx" in output, "Nginx is not running"
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check if Nginx is running")

def test_gateway_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode()
        assert "gateway" in output, "Gateway C++ backend is not running"
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check if gateway is running")

def test_https_endpoint_authorized():
    url = "https://127.0.0.1:8443/metrics"
    headers = {"Authorization": "Bearer SRE-SECRET-TOKEN"}
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        assert "downtime_events_total 5" in response.text, f"Expected 'downtime_events_total 5' in response, got '{response.text}'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTPS endpoint: {e}")

def test_https_endpoint_unauthorized():
    url = "https://127.0.0.1:8443/metrics"
    try:
        response = requests.get(url, verify=False, timeout=5)
        assert response.status_code == 401, f"Expected status 401, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTPS endpoint: {e}")