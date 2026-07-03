# test_final_state.py
import os
import subprocess
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"

def get_golden_hash(filepath):
    """Dynamically execute the binary to get the expected hash for a given file."""
    binary_path = "/app/hash_checker"
    assert os.path.isfile(binary_path), f"Missing binary {binary_path}"
    result = subprocess.run([binary_path, filepath], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def test_app1_config_success():
    filepath = "/home/user/deployments/app1/config.ini"
    response = requests.get(f"{BASE_URL}/status", params={"file": filepath})

    assert response.status_code == 200, f"Expected 200 OK for {filepath}, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "latest_update" in data, "Response JSON missing 'latest_update' key"
    assert "hash" in data, "Response JSON missing 'hash' key"

    expected_timestamp = "2023-10-05T15:30:00Z"
    expected_hash = get_golden_hash(filepath)

    assert data["latest_update"] == expected_timestamp, f"Expected timestamp {expected_timestamp}, got {data['latest_update']}"
    assert data["hash"] == expected_hash, f"Expected hash {expected_hash}, got {data['hash']}"

def test_app2_settings_success():
    filepath = "/home/user/deployments/app2/settings.ini"
    response = requests.get(f"{BASE_URL}/status", params={"file": filepath})

    assert response.status_code == 200, f"Expected 200 OK for {filepath}, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "latest_update" in data, "Response JSON missing 'latest_update' key"
    assert "hash" in data, "Response JSON missing 'hash' key"

    expected_timestamp = "2023-10-02T11:00:00Z"
    expected_hash = get_golden_hash(filepath)

    assert data["latest_update"] == expected_timestamp, f"Expected timestamp {expected_timestamp}, got {data['latest_update']}"
    assert data["hash"] == expected_hash, f"Expected hash {expected_hash}, got {data['hash']}"

def test_app3_ignore_not_group_writable():
    filepath = "/home/user/deployments/app3/ignore.ini"
    response = requests.get(f"{BASE_URL}/status", params={"file": filepath})

    assert response.status_code == 404, f"Expected 404 Not Found for {filepath} (not group-writable), got {response.status_code}"

def test_nonexistent_file():
    filepath = "/home/user/deployments/nonexistent.ini"
    response = requests.get(f"{BASE_URL}/status", params={"file": filepath})

    assert response.status_code == 404, f"Expected 404 Not Found for {filepath}, got {response.status_code}"