# test_final_state.py
import os
import time
import json
import urllib.request
import urllib.error
import subprocess
import pytest

def setup_module(module):
    script_path = "/home/user/start.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"start.sh failed with return code {result.returncode}.\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )

    # Wait for services to initialize
    time.sleep(3)

def test_nginx_config_exists():
    config_path = "/home/user/auth_util/nginx.conf"
    assert os.path.exists(config_path), f"Nginx configuration {config_path} is missing."

def test_valid_token():
    url = "http://localhost:8080/validate"
    data = json.dumps({"token": "SECURE_123"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}."

            headers = {k.lower(): v for k, v in response.getheaders()}
            assert "x-proxy-secure" in headers, "Header 'X-Proxy-Secure' is missing from the response."
            assert headers["x-proxy-secure"].lower() == "true", (
                f"Expected 'X-Proxy-Secure: true', got '{headers['x-proxy-secure']}'."
            )

            body = json.loads(response.read().decode("utf-8"))
            assert body.get("valid") is True, f"Expected {{'valid': true}}, got {body}."
    except urllib.error.URLError as e:
        pytest.fail(f"Request to {url} failed: {e}. Check if Nginx and the Rust API are running.")

def test_invalid_token():
    url = "http://localhost:8080/validate"
    data = json.dumps({"token": "INVALID_123"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}."

            body = json.loads(response.read().decode("utf-8"))
            assert body.get("valid") is False, f"Expected {{'valid': false}}, got {body}."
    except urllib.error.URLError as e:
        pytest.fail(f"Request to {url} failed: {e}. Check if Nginx and the Rust API are running.")

def test_admin_blocked():
    url = "http://localhost:8080/admin"
    req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req) as response:
            pytest.fail(f"Expected HTTP 403 for {url}, but got {response.status}.")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected HTTP 403 for /admin, got {e.code}."
    except urllib.error.URLError as e:
        pytest.fail(f"Request to {url} failed: {e}.")