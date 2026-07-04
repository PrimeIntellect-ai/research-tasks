# test_final_state.py

import os
import json
import ssl
import urllib.request
import urllib.error
import subprocess
import time
import pytest

def test_parsed_metrics_json():
    """Verify parsed_metrics.json exists and contains correct averages."""
    file_path = "/home/user/parsed_metrics.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_data = {
        "auth-service": 125,
        "billing-service": 307,
        "inventory-service": 47
    }
    assert data == expected_data, f"Content of {file_path} does not match expected metrics."

def test_tls_certs_exist():
    """Verify TLS certificates exist."""
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"
    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Key file {key_path} does not exist."

def test_secure_api_script_exists():
    """Verify secure_api.py exists."""
    script_path = "/home/user/secure_api.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_manage_services_script_exists_and_executable():
    """Verify manage_services.sh exists and is executable."""
    script_path = "/home/user/manage_services.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_https_server_response():
    """Verify the HTTPS server serves the metrics and handles 404 properly."""
    # Create an unverified context to bypass self-signed cert validation
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url_metrics = "https://localhost:9443/metrics"
    try:
        req = urllib.request.Request(url_metrics)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            content_type = response.headers.get("Content-Type", "")
            assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"
            data = json.loads(response.read().decode('utf-8'))
            expected_data = {
                "auth-service": 125,
                "billing-service": 307,
                "inventory-service": 47
            }
            assert data == expected_data, "API response does not match expected metrics."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url_metrics}: {e}")

    url_404 = "https://localhost:9443/invalid_path"
    try:
        req = urllib.request.Request(url_404)
        urllib.request.urlopen(req, context=ctx, timeout=5)
        pytest.fail("Expected 404 Not Found for invalid path, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 404, f"Expected status 404 for invalid path, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url_404}: {e}")

def test_manage_services_idempotency():
    """Verify manage_services.sh restarts the service and updates PID."""
    script_path = "/home/user/manage_services.sh"
    pid_file = "/home/user/api.pid"

    # Run script once
    subprocess.run([script_path], check=True)
    time.sleep(2) # Give it a moment to start and write PID

    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist after running script."
    with open(pid_file, "r") as f:
        pid1 = f.read().strip()

    assert pid1.isdigit(), f"PID file does not contain a valid PID: {pid1}"

    # Run script again
    subprocess.run([script_path], check=True)
    time.sleep(2)

    with open(pid_file, "r") as f:
        pid2 = f.read().strip()

    assert pid2.isdigit(), f"PID file does not contain a valid PID after restart: {pid2}"
    assert pid1 != pid2, "PID did not change after running manage_services.sh, service was not restarted."

    # Verify the new process is running
    try:
        os.kill(int(pid2), 0)
    except OSError:
        pytest.fail(f"Process with PID {pid2} is not running.")