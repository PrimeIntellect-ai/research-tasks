# test_final_state.py
import os
import requests
import pytest
import time

TOKEN = "773-ALPHA-991X"
BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_clean_docs_directory_exists():
    assert os.path.isdir("/home/user/clean_docs"), "Directory /home/user/clean_docs does not exist."

def test_unauthorized_access():
    url = f"{BASE_URL}/docs/server_migration.txt"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service at {BASE_URL}: {e}")
    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_authorized_access_and_sanitization_server_migration():
    url = f"{BASE_URL}/docs/server_migration.txt"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service at {BASE_URL}: {e}")
    assert response.status_code == 200, f"Expected 200 OK with valid token, got {response.status_code}"

    content = response.text
    assert "STATUS: ARCHIVED" in content, "STATUS: DRAFT was not replaced with STATUS: ARCHIVED"
    assert "STATUS: DRAFT" not in content, "STATUS: DRAFT is still present in the file"
    assert "Contact SSN: [REDACTED]" in content, "SSN was not properly redacted"
    assert "123-45-6789" not in content, "Original SSN is still present"

def test_authorized_access_and_sanitization_database_schema():
    url = f"{BASE_URL}/docs/database_schema.log"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service at {BASE_URL}: {e}")
    assert response.status_code == 200, f"Expected 200 OK with valid token, got {response.status_code}"

    content = response.text
    assert "STATUS: ARCHIVED" in content, "STATUS: DRAFT was not replaced with STATUS: ARCHIVED"
    assert "Backup operator SSN: [REDACTED]" in content, "SSN was not properly redacted"
    assert "987-65-4321" not in content, "Original SSN is still present"

def test_append_note_endpoint():
    url = f"{BASE_URL}/append_note"
    payload = {"file": "database_schema.log", "note": "Verified safe"}
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service at {BASE_URL}: {e}")
    assert response.status_code == 200, f"Expected 200 OK for POST /append_note, got {response.status_code}"

    # Verify the note was appended
    get_url = f"{BASE_URL}/docs/database_schema.log"
    try:
        get_response = requests.get(get_url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service at {BASE_URL}: {e}")

    assert get_response.status_code == 200
    content_lines = get_response.text.strip().split("\n")
    assert "Verified safe" in content_lines[-1], "The appended note was not found at the end of the file"