# test_final_state.py

import os
import subprocess
import requests
import pytest
import time

def test_keepalive_script_exists():
    path = "/home/user/keepalive.sh"
    assert os.path.isfile(path), f"Supervisor script {path} is missing."
    assert os.access(path, os.X_OK) or "bash" in open(path).read(), f"Supervisor script {path} should be executable or a bash script."

def test_crontab_configured():
    try:
        output = subprocess.check_output(["crontab", "-l"], text=True, stderr=subprocess.STDOUT)
        assert "keepalive.sh" in output, "crontab does not contain the keepalive script."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read crontab: {e.output}")

def test_nginx_config_fixed():
    path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "wrong_path.sock" not in content, "Nginx config still contains the broken proxy_pass directive."
    assert "backend.sock" in content, "Nginx config does not point to the new backend.sock."

def test_ssh_tunnel_active():
    try:
        output = subprocess.check_output(["ss", "-tlnp"], text=True)
        assert ":8888" in output, "No service is listening on port 8888 (SSH tunnel missing)."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check listening ports.")

def test_api_endpoint():
    url = "http://127.0.0.1:8888/pin"
    max_retries = 3
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                pytest.fail(f"Failed to connect to {url} after {max_retries} attempts.")
            time.sleep(1)
            continue

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
    assert data.get("pin") == "73925", f"Expected pin '73925', got {data.get('pin')}"