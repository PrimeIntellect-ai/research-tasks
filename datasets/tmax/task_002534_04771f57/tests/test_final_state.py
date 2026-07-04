# test_final_state.py

import os
import json
import sqlite3
import requests
import pytest

def test_sql_file_exists_and_valid():
    sql_path = "/home/user/optimized_graph.sql"
    assert os.path.isfile(sql_path), f"Optimized SQL file {sql_path} is missing."

    with open(sql_path, "r") as f:
        sql_content = f.read().strip()

    assert sql_content, f"SQL file {sql_path} is empty."

    # Ensure it's valid SQL by running it against the DB
    db_path = "/home/user/backups.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_content)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Executing the SQL query failed with error: {e}")
    finally:
        conn.close()

def test_http_service_response():
    url = "http://127.0.0.1:9090/impacted_backups"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Got: {response.text}")

    assert "corrupted_jobs" in data, "JSON response missing 'corrupted_jobs' key."
    assert "impacted_downstream_jobs" in data, "JSON response missing 'impacted_downstream_jobs' key."

    corrupted_jobs = sorted(data["corrupted_jobs"])
    impacted_jobs = sorted(data["impacted_downstream_jobs"])

    assert corrupted_jobs == [3, 8], f"Expected corrupted_jobs to be [3, 8], got {corrupted_jobs}"
    assert impacted_jobs == [4, 5, 9, 10], f"Expected impacted_downstream_jobs to be [4, 5, 9, 10], got {impacted_jobs}"