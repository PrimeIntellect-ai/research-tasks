# test_final_state.py

import os
import sqlite3
import subprocess
import requests
import pytest

DB_PATH = "/home/user/backups.db"
KEY_DERIVER_PATH = "/app/key_deriver"
URL = "http://127.0.0.1:8000/critical_keys"

def test_database_indexes():
    """Verify that an index was created on the deps table to optimize the query."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND tbl_name='deps';")
    indexes = cursor.fetchall()

    conn.close()

    assert len(indexes) > 0, "No indexes found on the 'deps' table. You must create an index to optimize the query."

def test_microservice_critical_keys():
    """Verify the microservice is running and returns the correct keys for the top 5 PageRank nodes."""
    try:
        response = requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the microservice at {URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    expected_jobs = ["job_42", "job_100", "job_333", "job_500", "job_777"]

    assert isinstance(data, dict), "Expected JSON response to be a dictionary"
    assert set(data.keys()) == set(expected_jobs), f"Expected keys {expected_jobs}, but got {list(data.keys())}"

    for job_id in expected_jobs:
        try:
            output = subprocess.check_output([KEY_DERIVER_PATH, job_id], text=True).strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to execute key_deriver for {job_id}: {e}")

        assert data[job_id] == output, f"Incorrect key for {job_id}. Expected {output}, got {data[job_id]}"