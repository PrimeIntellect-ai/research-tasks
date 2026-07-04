# test_final_state.py

import os
import time
import zipfile
import json
import requests
import hashlib
import pytest

def test_watchdog_fixed():
    events_py_path = "/app/watchdog-3.0.0/src/watchdog/events.py"
    assert os.path.exists(events_py_path), f"File {events_py_path} does not exist."
    with open(events_py_path, "r") as f:
        content = f.read()
    assert "import brokensystem_module" not in content, "The deliberate bug 'import brokensystem_module' is still present."

def test_dataset_server_behavior():
    incoming_dir = "/home/user/datasets/incoming"
    os.makedirs(incoming_dir, exist_ok=True)

    # 1. Create a valid zip file
    valid_zip_path = os.path.join(incoming_dir, "test_dataset.zip")
    with zipfile.ZipFile(valid_zip_path, 'w') as zf:
        zf.writestr("a.txt", "hello")
        zf.writestr("b.txt", "world")

    # 2. Create a corrupted zip file
    bad_zip_path = os.path.join(incoming_dir, "bad.zip")
    with open(bad_zip_path, 'w') as f:
        f.write("This is not a valid zip file")

    # Wait for the watchdog to process the files
    time.sleep(2)

    # 3. Request manifest for valid zip
    base_url = "http://127.0.0.1:8888/manifest"

    try:
        response_valid = requests.get(f"{base_url}?archive=test_dataset.zip", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the dataset server: {e}")

    assert response_valid.status_code == 200, f"Expected status code 200 for valid zip, got {response_valid.status_code}"

    try:
        manifest = response_valid.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON")

    expected_a_hash = hashlib.sha256(b"hello").hexdigest()
    expected_b_hash = hashlib.sha256(b"world").hexdigest()

    assert manifest.get("a.txt") == expected_a_hash, f"Hash for a.txt is incorrect, got {manifest.get('a.txt')}"
    assert manifest.get("b.txt") == expected_b_hash, f"Hash for b.txt is incorrect, got {manifest.get('b.txt')}"

    # 4. Request manifest for bad zip
    try:
        response_bad = requests.get(f"{base_url}?archive=bad.zip", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the dataset server: {e}")

    assert response_bad.status_code == 404, f"Expected status code 404 for bad zip, got {response_bad.status_code}"