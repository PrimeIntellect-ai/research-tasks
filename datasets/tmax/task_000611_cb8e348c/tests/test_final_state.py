# test_final_state.py

import os
import pytest
import requests

AUTH_TOKEN = "secr3t_lab_77xyz"
BASE_URL = "http://127.0.0.1:8000"

def test_recovered_archive_exists():
    """Verify that the recovered tar.gz file was created."""
    archive_path = "/home/user/recovered.tar.gz"
    assert os.path.isfile(archive_path), f"Recovered archive {archive_path} does not exist."
    assert os.path.getsize(archive_path) > 0, f"Recovered archive {archive_path} is empty."

def test_dataset_directory_exists_and_cleaned():
    """Verify that the dataset was extracted and cleaned correctly on disk."""
    dataset_dir = "/home/user/dataset"
    assert os.path.isdir(dataset_dir), f"Dataset directory {dataset_dir} does not exist."

    files = os.listdir(dataset_dir)
    assert len(files) > 0, "Dataset directory is empty."
    assert "log1.txt" in files, "log1.txt not found in extracted dataset."

    log1_path = os.path.join(dataset_dir, "log1.txt")
    with open(log1_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    assert "[ERR_CALIBRATION_LOSS]" not in content, "Found unreplaced '[ERR_CALIBRATION_LOSS]' in disk dataset."
    assert "SENSOR_NODE_00" not in content, "Found unreplaced 'SENSOR_NODE_00' in disk dataset."

def test_server_unauthorized_no_header():
    """Verify that the server rejects requests without an Authorization header."""
    url = f"{BASE_URL}/data/log1.txt"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without header, got {response.status_code}"

def test_server_unauthorized_wrong_header():
    """Verify that the server rejects requests with an incorrect Authorization header."""
    url = f"{BASE_URL}/data/log1.txt"
    headers = {"Authorization": "Bearer wrong_token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized with wrong header, got {response.status_code}"

def test_server_authorized_correct_header():
    """Verify that the server accepts requests with the correct Authorization header and returns cleaned data."""
    url = f"{BASE_URL}/data/log1.txt"
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK with correct header, got {response.status_code}"

    content = response.text
    assert "[ERR_CALIBRATION_LOSS]" not in content, "Response body contains uncleaned data: '[ERR_CALIBRATION_LOSS]'"
    assert "SENSOR_NODE_00" not in content, "Response body contains uncleaned data: 'SENSOR_NODE_00'"
    assert "NaN" in content or "NODE_0" in content, "Response body does not appear to contain the expected cleaned replacements."