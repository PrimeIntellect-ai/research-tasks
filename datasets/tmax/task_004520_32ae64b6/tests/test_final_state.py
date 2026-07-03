# test_final_state.py
import os
import urllib.request
import pytest

def test_service_flow():
    """Verify that Nginx, Flask, and Redis are correctly integrated and responding."""
    url = "http://127.0.0.1:8080/health"
    try:
        resp = urllib.request.urlopen(url, timeout=5)
        status = resp.status
        body = resp.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Service flow failed when trying to reach {url}: {e}")

    assert status == 200, f"Expected HTTP 200 from {url}, got {status}"
    assert body == "OK", f"Expected response body 'OK', got '{body}'"

def test_bundle_size():
    """Measure the total size of files in the deploy directory and assert it is below the threshold."""
    deploy_dir = "/app/deploy"
    assert os.path.isdir(deploy_dir), f"Deployment directory {deploy_dir} does not exist."

    total_size = sum(
        os.path.getsize(os.path.join(deploy_dir, f)) 
        for f in os.listdir(deploy_dir) 
        if os.path.isfile(os.path.join(deploy_dir, f))
    )

    threshold = 4096
    assert total_size < threshold, (
        f"Bundle size exceeds the allowed threshold. "
        f"Measured: {total_size} bytes, Threshold: {threshold} bytes."
    )

def test_deploy_status_log():
    """Check that the deploy_status.log file exists and contains the READY indicator."""
    log_path = "/home/user/deploy_status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read()

    assert "READY" in content, f"Expected the word 'READY' in {log_path}, but it was not found."