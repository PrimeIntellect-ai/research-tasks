# test_final_state.py

import os
import time
import subprocess
import requests
import pytest

def test_supervisor_conf_exists():
    """Check that the supervisor configuration file was created at the correct location."""
    conf_path = "/home/user/supervisor.conf"
    assert os.path.exists(conf_path), f"The supervisor configuration file {conf_path} does not exist."
    assert os.path.isfile(conf_path), f"The path {conf_path} is not a file."

def test_api_load_balancing():
    """
    Test that the SSH tunnel on port 8000 correctly forwards requests to the proxy,
    which injects the auth header and round-robins between port 8081 and 8082.
    """
    url = "http://127.0.0.1:8000/api/v1/manifests"
    backends_seen = set()

    # Send multiple requests to ensure both backends are hit
    for i in range(10):
        try:
            resp = requests.get(url, timeout=3)
            assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}. Response body: {resp.text}"

            try:
                data = resp.json()
            except ValueError:
                pytest.fail(f"Response was not valid JSON: {resp.text}")

            backend = data.get("backend")
            assert backend is not None, f"Response JSON missing 'backend' field: {data}"
            backends_seen.add(backend)

        except requests.RequestException as e:
            pytest.fail(f"Request to {url} failed: {e}")

    assert "port-8081" in backends_seen, "After 10 requests, did not receive any response from backend port-8081. Load balancing might not be working."
    assert "port-8082" in backends_seen, "After 10 requests, did not receive any response from backend port-8082. Load balancing might not be working."

def test_process_supervision():
    """
    Test that killing the proxy script results in supervisord restarting it,
    restoring service availability.
    """
    # Attempt to kill the proxy process
    subprocess.run(["pkill", "-9", "-f", "proxy.py"])

    # Give supervisord some time to detect the crash and restart the process
    time.sleep(5)

    url = "http://127.0.0.1:8000/api/v1/manifests"
    try:
        resp = requests.get(url, timeout=5)
        assert resp.status_code == 200, f"Service did not recover after proxy was killed. Expected 200 OK, got {resp.status_code}."
    except requests.RequestException as e:
        pytest.fail(f"Service did not recover after proxy was killed. Request failed: {e}")