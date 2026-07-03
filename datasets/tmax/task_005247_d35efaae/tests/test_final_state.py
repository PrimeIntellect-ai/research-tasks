# test_final_state.py

import os
import stat
import pytest
import requests
import time

def test_config_ini_exists_and_correct():
    config_path = "/home/user/telemetryd/config.ini"
    assert os.path.isfile(config_path), f"Configuration file {config_path} is missing."

    with open(config_path, "r") as f:
        content = f.read()

    assert "PORT=8088" in content, "config.ini does not contain the correct PORT."
    assert "AUTH_TOKEN=f9a3b2c1-telemetry-token" in content, "config.ini does not contain the correct AUTH_TOKEN."

def test_regression_script_exists_and_executable():
    script_path = "/home/user/telemetryd/test_regression.sh"
    assert os.path.isfile(script_path), f"Regression test script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Regression test script {script_path} is not executable."

def test_telemetry_server_running_and_healthy():
    url = "http://127.0.0.1:8088/health"
    headers = {
        "Authorization": "Bearer f9a3b2c1-telemetry-token"
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=2)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    else:
        pytest.fail("Failed to connect to the telemetry server or did not receive a 200 OK response. Ensure the server is running on port 8088 and not crashing.")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
        assert data.get("status") == "healthy", f"Expected response body to have status 'healthy', got {data}"
    except ValueError:
        assert "healthy" in response.text.lower(), f"Expected 'healthy' in response body, got {response.text}"