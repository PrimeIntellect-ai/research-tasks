# test_final_state.py

import os
import re
import time
import pytest
import requests

def test_manifest_file_exists():
    """Test that the deployment manifest file was created."""
    manifest_path = "/home/user/deployment.yaml"
    assert os.path.isfile(manifest_path), f"Manifest file is missing: {manifest_path}"

def test_manifest_content():
    """Test that the deployment manifest contains the correct values."""
    manifest_path = "/home/user/deployment.yaml"
    with open(manifest_path, "r") as f:
        content = f.read()

    assert re.search(r"kind:\s*Deployment", content), "Manifest missing 'kind: Deployment'"
    assert re.search(r"name:\s*cache-deployment", content), "Manifest missing 'metadata.name: cache-deployment'"
    assert re.search(r"replicas:\s*4", content), "Manifest missing 'spec.replicas: 4'"
    assert re.search(r"image:\s*redis:6\.0", content), "Manifest missing 'image: redis:6.0'"
    assert re.search(r"name:\s*cache", content), "Manifest missing container 'name: cache'"

def test_web_service_and_log_rotation():
    """Test the web service endpoint, response headers, and log rotation."""
    url = "http://127.0.0.1:8080/manifest.yaml"

    # Make a single request to verify the response
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/x-yaml" in content_type, f"Expected Content-Type 'application/x-yaml', got '{content_type}'"

    content = response.text
    assert re.search(r"replicas:\s*4", content), "Response missing 'replicas: 4'"
    assert re.search(r"image:\s*redis:6\.0", content), "Response missing 'image: redis:6.0'"

    # Make enough requests to trigger log rotation (assuming each log line is at least 20 bytes, 100 requests > 2000 bytes)
    for _ in range(100):
        requests.get(url, timeout=2)

    # Allow a brief moment for the logger to flush and rotate if asynchronous
    time.sleep(1)

    log_file = "/home/user/service.log"
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    # Check that log rotation occurred and file sizes are within limits
    assert os.path.getsize(log_file) <= 1024, f"{log_file} exceeds 1024 bytes"

    backup_log_1 = "/home/user/service.log.1"
    assert os.path.isfile(backup_log_1), f"Backup log file missing: {backup_log_1}. Log rotation may not be working."
    assert os.path.getsize(backup_log_1) <= 1024, f"{backup_log_1} exceeds 1024 bytes"