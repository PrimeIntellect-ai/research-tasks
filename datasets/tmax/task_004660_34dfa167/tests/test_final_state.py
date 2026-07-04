# test_final_state.py

import json
import sqlite3
import requests
import pytest

URL = "http://127.0.0.1:9050/api/audit"
TOKEN = "secret123"

def get_expected_data():
    db_path = "/app/logs.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT u.id, u.email, COUNT(l.id) as failed_attempts
    FROM users u
    JOIN logins l ON u.id = l.user_id
    WHERE l.status = 'FAILED'
      AND json_extract(u.metadata, '$.department') = 'Engineering'
    GROUP BY u.id
    HAVING failed_attempts > 3
    ORDER BY failed_attempts DESC, u.id ASC
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "user_id": row[0],
            "email": row[1],
            "failed_attempts": row[2]
        }
        for row in rows
    ]

def test_unauthorized_request():
    """Test that requests without the correct Bearer token are rejected with a 401."""
    try:
        response = requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}. Response: {response.text}"

    headers = {"Authorization": "Bearer wrong_token"}
    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized with wrong token, got {response.status_code}. Response: {response.text}"

def test_authorized_request():
    """Test that authorized requests return the correct JSON data."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK with correct token, got {response.status_code}. Response: {response.text}"

    try:
        actual_data = response.json()
    except ValueError:
        pytest.fail(f"Service did not return valid JSON. Response text: {response.text}")

    expected_data = get_expected_data()

    assert actual_data == expected_data, f"JSON response mismatch.\nExpected: {expected_data}\nActual: {actual_data}"