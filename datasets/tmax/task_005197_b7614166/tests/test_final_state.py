# test_final_state.py
import pytest
import sqlite3
import requests
import time

def test_database_index():
    """Verify that an index was created on the transfers table."""
    conn = sqlite3.connect('/app/finance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='transfers'")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No index was created on the 'transfers' table. An index strategy was required."

def test_http_service_unauthorized():
    """Verify the service returns 403 when the auth header is missing."""
    url = "http://127.0.0.1:9000/chain"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service at {url}: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden without auth header, got {response.status_code}"

def test_http_service_authorized():
    """Verify the service returns the correct JSON array when authorized."""
    url = "http://127.0.0.1:9000/chain"
    headers = {"X-Compliance-Auth": "auditor_key"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK with auth header, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    expected_accounts = ["10002", "10003", "10004", "10005", "10006"]
    assert isinstance(data, list), "Expected a JSON array"
    assert data == expected_accounts, f"Expected account list {expected_accounts}, got {data}"