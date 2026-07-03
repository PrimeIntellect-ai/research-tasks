# test_final_state.py

import os
import time
import glob
import subprocess
import requests
import pytest

def test_script_exists():
    """Verify that the deployment script exists."""
    assert os.path.isfile("/home/user/edge_deploy.sh"), "Deployment script /home/user/edge_deploy.sh not found."

def test_binary_compiled():
    """Verify that the edgetelem binary was compiled successfully."""
    assert os.path.isfile("/app/edgetelem-1.2.0/edgetelem"), "Compiled binary /app/edgetelem-1.2.0/edgetelem not found."
    assert os.access("/app/edgetelem-1.2.0/edgetelem", os.X_OK), "edgetelem is not executable."

def test_service_integration():
    """
    Integration test to verify:
    1. Service is running and responds to /ping.
    2. Service accepts /submit and logs data.
    3. Watchdog rotates log when > 100 bytes.
    4. Watchdog restarts service when killed.
    """
    base_url = "http://127.0.0.1:8080"

    # 1. Check if service is up
    try:
        resp = requests.get(f"{base_url}/ping", timeout=2)
        assert resp.status_code == 200, f"Expected 200 OK for /ping, got {resp.status_code}"
        assert "pong" in resp.text.lower(), f"Expected 'pong' in response, got {resp.text}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to service at {base_url}/ping: {e}")

    # 2. Trigger backup by sending POST requests until > 100 bytes
    payload = '{"sensor": "temp", "value": 22.5}\n'
    # Send enough requests to exceed 100 bytes. Each payload is ~34 bytes.
    # 4 requests = 136 bytes.
    for _ in range(5):
        try:
            resp = requests.post(f"{base_url}/submit", data=payload, headers={"Content-Type": "application/json"}, timeout=2)
            assert resp.status_code == 200, f"Expected 200 OK for /submit, got {resp.status_code}"
        except requests.RequestException as e:
            pytest.fail(f"Failed to POST to {base_url}/submit: {e}")

    # 3. Wait for watchdog to rotate the log
    time.sleep(3)

    backups = glob.glob("/home/user/backups/telemetry-*.bak")
    assert len(backups) > 0, "No backup files found in /home/user/backups/ after exceeding 100 bytes."

    # Check that at least one backup contains our payload
    found_payload = False
    for backup in backups:
        with open(backup, "r") as f:
            content = f.read()
            if "sensor" in content and "temp" in content:
                found_payload = True
                break
    assert found_payload, "Backup file was created but does not contain the submitted telemetry data."

    # 4. Kill the process and verify watchdog restarts it
    try:
        subprocess.run(["killall", "edgetelem"], check=False)
    except Exception as e:
        pytest.fail(f"Failed to execute killall: {e}")

    # Wait for watchdog to detect and restart (watchdog checks every ~1s)
    time.sleep(4)

    try:
        resp = requests.get(f"{base_url}/ping", timeout=2)
        assert resp.status_code == 200, f"Service did not recover after being killed. Expected 200 OK, got {resp.status_code}"
        assert "pong" in resp.text.lower(), "Service recovered but returned unexpected response to /ping."
    except requests.RequestException as e:
        pytest.fail(f"Service failed to restart after being killed. Watchdog script is not working correctly. Error: {e}")