# test_final_state.py
import os
import sqlite3
import requests
import pytest

DB_PATH = "/home/user/cleaned.db"
BASE_URL = "http://127.0.0.1:8080"
AUTH_TOKEN = "X9F2-K1M8"
TABLE_NAME = "active_users"

def test_sqlite_db_exists():
    """Verify that the SQLite database file was created at the expected path."""
    assert os.path.exists(DB_PATH), f"SQLite database not found at {DB_PATH}"

def test_sqlite_table_exists():
    """Verify that the SQLite database contains the correct table name extracted via OCR."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (TABLE_NAME,))
    table = cursor.fetchone()
    conn.close()
    assert table is not None, f"Table '{TABLE_NAME}' not found in SQLite database. Ensure OCR extraction was successful."

def test_http_endpoint_auth_missing():
    """Verify that omitting the Authorization header results in a 401 Unauthorized."""
    try:
        response = requests.get(f"{BASE_URL}/user/1", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {response.status_code}"

def test_http_endpoint_auth_wrong():
    """Verify that providing an incorrect Authorization header results in a 401 Unauthorized."""
    headers = {"Authorization": "Bearer INVALID-TOKEN"}
    try:
        response = requests.get(f"{BASE_URL}/user/1", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for wrong auth, got {response.status_code}"

def test_http_endpoint_success_user_1():
    """Verify that user 1 data is correctly cleaned, deduplicated, joined, and returned."""
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        response = requests.get(f"{BASE_URL}/user/1", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert int(data.get("user_id", 0)) == 1, f"Incorrect user_id: {data.get('user_id')}"
    assert data.get("name") == "José", f"Incorrect name (unicode cleaning failed), expected 'José', got {data.get('name')}"
    assert int(data.get("timestamp", 0)) == 200, f"Incorrect timestamp (deduplication failed), expected 200, got {data.get('timestamp')}"
    assert data.get("status") == "active", f"Incorrect status (join failed), expected 'active', got {data.get('status')}"
    assert int(data.get("score", 0)) == 99, f"Incorrect score (join failed), expected 99, got {data.get('score')}"

def test_http_endpoint_success_user_2():
    """Verify that user 2 data is correctly cleaned, joined, and returned."""
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        response = requests.get(f"{BASE_URL}/user/2", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert int(data.get("user_id", 0)) == 2, f"Incorrect user_id: {data.get('user_id')}"
    assert data.get("name") == "Réne", f"Incorrect name (unicode cleaning failed), expected 'Réne', got {data.get('name')}"
    assert int(data.get("timestamp", 0)) == 150, f"Incorrect timestamp, expected 150, got {data.get('timestamp')}"
    assert data.get("status") == "inactive", f"Incorrect status (join failed), expected 'inactive', got {data.get('status')}"
    assert int(data.get("score", 0)) == 45, f"Incorrect score (join failed), expected 45, got {data.get('score')}"