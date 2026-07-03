# test_final_state.py

import os
import sqlite3
import pytest
import requests

def test_database_schema():
    db_path = "/home/user/app.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(users);")
    columns = cursor.fetchall()

    assert len(columns) > 0, "Table 'users' does not exist or has no columns."

    column_names = [col[1] for col in columns]
    assert "id" in column_names, "Column 'id' is missing from 'users' table."
    assert "name" in column_names, "Column 'name' is missing from 'users' table."
    assert "email" in column_names, "Column 'email' is missing from 'users' table."

    conn.close()

def test_python_server_compute_endpoint():
    url = "http://127.0.0.1:7331/compute"
    headers = {
        "X-API-Key": "tesseract_secret_99",
        "Content-Type": "application/json"
    }
    payload = {"a": 42, "b": 58}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Python server or request failed: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "result" in data, f"Expected 'result' in response JSON, got: {data}"
    assert data["result"] == 100, f"Expected result to be 100, got {data['result']}"

def test_python_server_unauthorized():
    url = "http://127.0.0.1:7331/compute"
    headers = {
        "X-API-Key": "wrong_key",
        "Content-Type": "application/json"
    }
    payload = {"a": 10, "b": 15}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Python server or request failed: {e}")

    assert response.status_code in (401, 403), f"Expected status code 401 or 403 for unauthorized request, got {response.status_code}"