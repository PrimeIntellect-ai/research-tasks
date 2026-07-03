# test_final_state.py
import os
import sqlite3
import subprocess
import requests
import time
import pytest

def test_recovered_db_exists_and_valid():
    db_path = "/home/user/recovered.db"
    assert os.path.exists(db_path), f"Recovered database not found at {db_path}"

    # Check if the database has the expected 142 records
    # We don't know the exact table name, but we can query sqlite_master or just rely on the API count.
    # The API count is explicitly verified later.

def test_mre_script():
    mre_path = "/home/user/mre.py"
    assert os.path.exists(mre_path), f"MRE script not found at {mre_path}"

    # Run the MRE script
    result = subprocess.run(
        ["python3", mre_path],
        capture_output=True,
        text=True
    )

    # The MRE should attempt the database operation on /home/user/test.db
    test_db_path = "/home/user/test.db"
    assert os.path.exists(test_db_path), f"MRE script did not create {test_db_path}"

    # Check if some sqlite3 error was mentioned in the output or stderr
    output = result.stdout.lower() + result.stderr.lower()
    assert "error" in output or "exception" in output or result.returncode != 0, "MRE script did not seem to reproduce an error."

def test_service_health():
    url = "http://127.0.0.1:8080/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()
    assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"

def test_service_frames_count():
    url = "http://127.0.0.1:8080/api/frames/count"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()
    assert data.get("count") == 142, f"Expected {{'count': 142}}, got {data}"