# test_final_state.py

import os
import json
import pytest
import requests

def test_decrypted_logs_exist():
    """Verify that the decrypted logs file was created and contains valid JSON."""
    path = "/home/user/decrypted_logs.json"
    assert os.path.isfile(path), f"Expected file {path} is missing. Did you run your decryption script?"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
            assert isinstance(data, list), "Decrypted logs should be a JSON array."
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

def test_decrypt_script_exists():
    """Verify that the decrypt script was written."""
    path = "/home/user/decrypt_logs.py"
    assert os.path.isfile(path), f"Expected file {path} is missing."

def test_secure_proxy_authorized():
    """Test that the secure proxy returns the decrypted log entry for an authorized request."""
    url = "http://127.0.0.1:9000/compliance?id=1"
    headers = {"Authorization": "Bearer COMPLIANCE_SECURE_TOKEN"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to secure proxy at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from proxy, got: {response.text}")

    assert "id" in data, "Response JSON missing 'id' field."
    assert str(data["id"]) == "1", f"Expected id 1, got {data['id']}"
    assert "action" in data, "Response JSON missing 'action' field."
    assert "user" in data, "Response JSON missing 'user' field."

def test_secure_proxy_unauthorized():
    """Test that the secure proxy rejects unauthorized requests."""
    url = "http://127.0.0.1:9000/compliance?id=1"

    # Test with missing header
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to secure proxy at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for missing token, got {response.status_code}."

    # Test with wrong header
    headers = {"Authorization": "Bearer INVALID_TOKEN"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to secure proxy at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for invalid token, got {response.status_code}."

def test_sql_injection_remediated():
    """Test that the SQL injection vulnerability in log-ingest has been fixed."""
    url = "http://127.0.0.1:5002/search"
    params = {"user": "admin' OR 1=1 --"}

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to log-ingest service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from search endpoint, got: {response.text}")

    # If it's returning all records due to injection, the list will be large.
    # If fixed, it should return 0 results (or just one if a user literally has that name, which is unlikely).
    # We assume the DB has multiple records. If injection works, it returns multiple records.
    assert isinstance(data, list), "Expected JSON response to be a list."
    assert len(data) <= 1, "SQL injection appears to still be present; returned multiple records for an invalid username."