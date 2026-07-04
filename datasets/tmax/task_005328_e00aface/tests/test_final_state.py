# test_final_state.py
import os
import time
import glob
import tarfile
import requests
import pytest

URL = "http://127.0.0.1:8080/apply"
TOKEN = "Bearer k8s-operator-token-123"

VALID_YAML = """apiVersion: v1
kind: Deployment
metadata:
  name: test-app
spec:
  replicas: 4
"""

INVALID_YAML = """apiVersion: v1
kind: Deployment
metadata:
  name: bad-app
"""

def test_operator_valid_request():
    headers = {"Authorization": TOKEN}
    try:
        response = requests.post(URL, headers=headers, data=VALID_YAML, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to operator: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    assert response.text.strip() == "COMPILED:test-app:8", f"Unexpected response body: {response.text}"

def test_operator_unauthorized():
    try:
        response = requests.post(URL, data=VALID_YAML, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to operator: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for missing token, got {response.status_code}"

def test_operator_invalid_request():
    headers = {"Authorization": TOKEN}
    try:
        response = requests.post(URL, headers=headers, data=INVALID_YAML, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to operator: {e}")

    assert response.status_code == 400, f"Expected HTTP 400 Bad Request for compiler failure, got {response.status_code}"

def test_manifest_saved():
    manifest_path = "/home/user/manifests/test-app.yaml"
    assert os.path.exists(manifest_path), f"Manifest was not saved to {manifest_path}"
    with open(manifest_path, "r") as f:
        content = f.read()
    assert "test-app" in content, "Saved manifest does not contain the expected content"

def test_backups_created_and_rotated():
    # Wait a few seconds to ensure backups are generated
    time.sleep(5)

    backup_dir = "/home/user/backups"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist"

    backups = glob.glob(os.path.join(backup_dir, "backup_*.tar.gz"))
    assert len(backups) > 0, "No backups found in the backup directory"
    assert len(backups) <= 3, f"Expected at most 3 backups, found {len(backups)}"

    # Check if the latest backup contains the manifest
    latest_backup = max(backups, key=os.path.getmtime)

    with tarfile.open(latest_backup, "r:gz") as tar:
        names = tar.getnames()
        # The tarball should contain the manifests directory or files inside it
        has_manifest = any("test-app.yaml" in name for name in names)
        assert has_manifest, f"Manifest 'test-app.yaml' not found in backup {latest_backup}"