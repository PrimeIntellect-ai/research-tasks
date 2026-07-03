# test_final_state.py

import os
import requests
import pytest

API_URL = "http://127.0.0.1:8080"
STORAGE_URL = "http://127.0.0.1:9000"

def test_env_file_updated():
    """Verify that the .env file points to the correct storage backend URL."""
    env_path = "/app/recovery_api/.env"
    assert os.path.isfile(env_path), f"Expected .env file is missing: {env_path}"

    with open(env_path, "r") as f:
        content = f.read()

    # Strip quotes just in case they were added
    normalized_content = content.replace("'", "").replace('"', "")
    assert "STORAGE_URL=http://127.0.0.1:9000" in normalized_content, "STORAGE_URL in .env is not correctly pointing to the Python storage backend."

def test_storage_backend_running():
    """Verify the Python storage backend is running on port 9000."""
    try:
        response = requests.get(f"{STORAGE_URL}/", timeout=3)
        # We just want to know it's accepting connections, even if it returns 404 for root
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Could not connect to the Python storage backend on port 9000: {e}")

def test_recover_endpoint():
    """Test 1: End-to-End Flow for /recover"""
    try:
        response = requests.post(
            f"{API_URL}/recover",
            json={"evidence_id": "log_01"},
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Could not connect to the Rust recovery API on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for /recover, got {response.status_code}. Response body: {response.text}"
    assert "EVIDENCE_FOUND_SYSTEM_COMPROMISED" in response.text, f"Expected decrypted content not found in response. Response body: {response.text}"

def test_export_path_traversal_mitigation():
    """Test 2: CWE-22 Mitigation for /export"""
    try:
        response = requests.post(
            f"{API_URL}/export",
            json={"filename": "../evil.sh", "data": "test"},
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Could not connect to the Rust recovery API on port 8080: {e}")

    assert response.status_code in (400, 403), f"Expected HTTP 400 or 403 for path traversal attempt, got {response.status_code}. Response body: {response.text}"

def test_export_safe_file():
    """Test 3: Safe Export for /export"""
    try:
        response = requests.post(
            f"{API_URL}/export",
            json={"filename": "evidence.txt", "data": "test_safe_export_data"},
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Could not connect to the Rust recovery API on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for safe export, got {response.status_code}. Response body: {response.text}"

    # Verify file was successfully written to the correct directory
    export_path = "/app/recovery_api/exports/evidence.txt"
    assert os.path.isfile(export_path), f"Export file was not created at the expected path: {export_path}"

    with open(export_path, "r") as f:
        content = f.read()

    assert content == "test_safe_export_data", f"Expected file content 'test_safe_export_data', got '{content}'"