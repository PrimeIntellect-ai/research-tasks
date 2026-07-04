# test_final_state.py

import os
import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"
DATASTORE_DIR = "/home/user/datastore"

def test_datastore_directory_exists():
    assert os.path.exists(DATASTORE_DIR), f"Directory {DATASTORE_DIR} does not exist."
    assert os.path.isdir(DATASTORE_DIR), f"Path {DATASTORE_DIR} is not a directory."

def verify_process_endpoint(sec: int):
    # Initial request
    url = f"{BASE_URL}/process?sec={sec}"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "second" in data, "JSON response missing 'second' field"
    assert "size" in data, "JSON response missing 'size' field"
    assert "classification" in data, "JSON response missing 'classification' field"

    assert data["second"] == sec, f"Expected second {sec}, got {data['second']}"

    # Check file exists
    frame_path = os.path.join(DATASTORE_DIR, f"frame_{sec}.jpg")
    assert os.path.exists(frame_path), f"Frame image {frame_path} was not created."

    # Verify size
    actual_size = os.path.getsize(frame_path)
    assert data["size"] == actual_size, f"JSON size {data['size']} does not match actual file size {actual_size}"

    # Verify classification
    expected_classification = "Complex" if actual_size > 40000 else "Simple"
    assert data["classification"] == expected_classification, f"Expected classification '{expected_classification}', got '{data['classification']}'"

    return frame_path

def test_process_sec_2():
    frame_path = verify_process_endpoint(2)

    # Check caching behavior
    mtime_before = os.path.getmtime(frame_path)

    # Wait briefly to ensure mtime would change if rewritten
    time.sleep(1)

    url = f"{BASE_URL}/process?sec=2"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200

    mtime_after = os.path.getmtime(frame_path)
    assert mtime_before == mtime_after, "File modification time changed, indicating the frame was not cached."

def test_process_sec_15():
    verify_process_endpoint(15)