# test_final_state.py

import os
import stat
import subprocess
import time
import urllib.request
import urllib.error
import json
import pytest

WORKDIR = "/home/user/manifest-operator"

def test_files_exist_and_executable():
    """Verify that all required files exist and monitor.sh is executable."""
    assert os.path.isdir(WORKDIR), f"Directory {WORKDIR} does not exist."

    backend_go = os.path.join(WORKDIR, "backend.go")
    proxy_go = os.path.join(WORKDIR, "proxy.go")
    monitor_sh = os.path.join(WORKDIR, "monitor.sh")

    assert os.path.isfile(backend_go), f"{backend_go} does not exist."
    assert os.path.isfile(proxy_go), f"{proxy_go} does not exist."
    assert os.path.isfile(monitor_sh), f"{monitor_sh} does not exist."

    st = os.stat(monitor_sh)
    assert bool(st.st_mode & stat.S_IXUSR), f"{monitor_sh} is not executable."

def test_cron_job_configured():
    """Verify that the cron job is configured correctly."""
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab or crontab is empty.")

    expected_cron = "* * * * * /home/user/manifest-operator/monitor.sh"
    assert expected_cron in output, f"Cron job not found in crontab. Expected: {expected_cron}"

def test_services_running():
    """Run monitor.sh and verify ports 8080 and 8081 are listening."""
    # Execute monitor.sh to ensure services are up
    subprocess.run([os.path.join(WORKDIR, "monitor.sh")], cwd=WORKDIR, check=False)
    time.sleep(3)  # Give them time to start

    try:
        ss_output = subprocess.check_output(["ss", "-tln"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ss command.")

    assert ":8081" in ss_output, "Backend service is not listening on port 8081."
    assert ":8080" in ss_output, "Proxy service is not listening on port 8080."

def test_proxy_and_backend_logic():
    """Test the proxy and backend logic with valid and invalid payloads."""
    backend_log = os.path.join(WORKDIR, "backend.log")
    proxy_log = os.path.join(WORKDIR, "proxy.log")

    # Clear logs if they exist
    if os.path.exists(backend_log):
        os.remove(backend_log)
    if os.path.exists(proxy_log):
        os.remove(proxy_log)

    # Test 1: Valid payload
    valid_payload = json.dumps({"metadata": {"annotations": {"proxy.local/managed": "true"}}}).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8080/apply", data=valid_payload, method="POST", headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Valid request failed: {e}")

    time.sleep(1)

    assert os.path.isfile(backend_log), "backend.log was not created."
    with open(backend_log, 'r') as f:
        backend_content = f.read()
    expected_log = f"ACCEPTED: {len(valid_payload)} bytes"
    assert expected_log in backend_content, f"Expected '{expected_log}' in backend.log, got: {backend_content}"

    # Test 2: Invalid payload (missing annotation)
    invalid_payload_1 = json.dumps({"metadata": {"annotations": {}}}).encode('utf-8')
    req2 = urllib.request.Request("http://127.0.0.1:8080/apply", data=invalid_payload_1, method="POST", headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req2)
        pytest.fail("Expected 403 Forbidden for missing annotation, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected 403 Forbidden, got {e.code}"

    time.sleep(1)

    assert os.path.isfile(proxy_log), "proxy.log was not created."
    with open(proxy_log, 'r') as f:
        proxy_content = f.read()
    assert "REJECTED" in proxy_content, "Expected 'REJECTED' in proxy.log"

    # Test 3: Invalid payload (wrong value)
    invalid_payload_2 = json.dumps({"metadata": {"annotations": {"proxy.local/managed": "false"}}}).encode('utf-8')
    req3 = urllib.request.Request("http://127.0.0.1:8080/apply", data=invalid_payload_2, method="POST", headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req3)
        pytest.fail("Expected 403 Forbidden for wrong annotation value, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected 403 Forbidden, got {e.code}"

    time.sleep(1)

    with open(proxy_log, 'r') as f:
        proxy_content = f.read()
    assert proxy_content.count("REJECTED") >= 2, "Expected at least 2 'REJECTED' lines in proxy.log"