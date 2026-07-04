# test_final_state.py

import os
import sqlite3
import subprocess
import requests
import pytest

DB_PATH = "/home/user/telemetry.db"
SCRIPT_PATH = "/home/user/export_db.sh"
URL = "http://127.0.0.1:8000/data"
TOKEN = "crimson sky"

EXPECTED_DATA = {
    1: {"calibrated_reading": 20.0, "rolling_avg": 20.0},
    2: {"calibrated_reading": 40.0, "rolling_avg": 30.0},
    3: {"calibrated_reading": 60.0, "rolling_avg": 40.0},
    4: {"calibrated_reading": 80.0, "rolling_avg": 60.0},
    5: {"calibrated_reading": 100.0, "rolling_avg": 80.0},
    6: {"calibrated_reading": 120.0, "rolling_avg": 100.0},
}

def test_database_exists_and_has_data():
    """Check if the SQLite database exists and has the correct processed data."""
    assert os.path.exists(DB_PATH), f"Database not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processed_data'")
    assert cursor.fetchone() is not None, "Table 'processed_data' does not exist in the database."

    # Check data
    cursor.execute("SELECT timestamp, calibrated_reading, rolling_avg FROM processed_data ORDER BY timestamp")
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) >= 6, "Not enough rows in the processed_data table."

    for row in rows:
        ts = int(row[0])
        if ts in EXPECTED_DATA:
            expected = EXPECTED_DATA[ts]
            assert abs(row[1] - expected["calibrated_reading"]) < 1e-5, f"Incorrect calibrated_reading for timestamp {ts}"
            assert abs(row[2] - expected["rolling_avg"]) < 1e-5, f"Incorrect rolling_avg for timestamp {ts}"

def test_web_service_auth_and_data():
    """Check if the web service is running, requires auth, and returns correct data."""
    # Test without auth
    try:
        response = requests.get(f"{URL}?timestamp=3", timeout=2)
        assert response.status_code in [401, 403], f"Expected 401/403 without auth, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Web service is not running or not reachable on 127.0.0.1:8000")

    # Test with wrong auth
    headers = {"Authorization": "Bearer wrong token"}
    response = requests.get(f"{URL}?timestamp=3", headers=headers, timeout=2)
    assert response.status_code in [401, 403], f"Expected 401/403 with wrong auth, got {response.status_code}"

    # Test with correct auth
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{URL}?timestamp=3", headers=headers, timeout=2)
    assert response.status_code == 200, f"Expected 200 OK with correct auth, got {response.status_code}"

    data = response.json()
    assert data.get("timestamp") == 3, "Incorrect timestamp in response"
    assert abs(data.get("calibrated_reading", 0) - 60.0) < 1e-5, "Incorrect calibrated_reading in response"
    assert abs(data.get("rolling_avg", 0) - 40.0) < 1e-5, "Incorrect rolling_avg in response"

def test_cron_script_exists():
    """Check if the export shell script exists."""
    assert os.path.exists(SCRIPT_PATH), f"Export script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK) or os.access(SCRIPT_PATH, os.R_OK), "Export script should be readable/executable"

def test_crontab_configured():
    """Check if the crontab is configured to run every 15 minutes."""
    try:
        result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        try:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
            crontab_content = result.stdout
        except subprocess.CalledProcessError:
            pytest.fail("Failed to read crontab")

    # Check for 15-minute interval
    valid_patterns = ["*/15", "0,15,30,45", "00,15,30,45"]
    found = False
    for line in crontab_content.splitlines():
        if SCRIPT_PATH in line and not line.strip().startswith("#"):
            parts = line.split()
            if len(parts) >= 5 and any(p in parts[0] for p in valid_patterns):
                found = True
                break

    assert found, "Crontab is not configured to run the script every 15 minutes."