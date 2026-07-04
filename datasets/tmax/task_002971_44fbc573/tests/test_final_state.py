# test_final_state.py
import os
import time
import subprocess
import requests
import pytest
import csv

def test_api_is_running():
    """Ensure the API is up and running after fixing Docker Compose files."""
    try:
        res = requests.get("http://localhost:8000/health", timeout=5)
        assert res.status_code == 200, f"API health endpoint returned {res.status_code} instead of 200"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API on http://localhost:8000/health: {e}")

def test_health_monitor_script():
    """Ensure the health monitor script exists and has logged [OK] statuses."""
    script_path = "/home/user/health_monitor.sh"
    log_path = "/home/user/api_health.log"

    assert os.path.isfile(script_path), f"Missing shell script at {script_path}"

    assert os.path.isfile(log_path), f"Missing log file at {log_path}. Ensure the script is running in the background."
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "[OK]" in content, f"Log {log_path} does not contain any '[OK]' entries. Is the API healthy and the script running?"

def test_clean_users_csv():
    """Ensure the legacy data was parsed correctly into a CSV with 5000 rows plus header."""
    csv_path = "/home/user/clean_users.csv"
    assert os.path.isfile(csv_path), f"Missing extracted CSV file at {csv_path}"

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 5001, f"Expected exactly 5001 rows (1 header + 5000 data rows), but got {len(rows)}"

    header = [c.strip() for c in rows[0]]
    assert header == ["username", "email", "role"], f"Incorrect CSV header. Expected ['username', 'email', 'role'], got {header}"

def test_import_users_performance():
    """
    Ensure the import script runs successfully and completes within the 12.0 second threshold
    by utilizing concurrency.
    """
    script_path = "/home/user/import_users.py"
    assert os.path.isfile(script_path), f"Missing Python import script at {script_path}"

    # Clear DB to ensure a fresh test environment
    try:
        del_res = requests.delete("http://localhost:8000/users", timeout=5)
        del_res.raise_for_status()
    except Exception as e:
        pytest.fail(f"Failed to clear the database prior to testing import: {e}")

    # Measure execution time
    start = time.time()
    res = subprocess.run(["python3", script_path], capture_output=True, text=True)
    duration = time.time() - start

    assert res.returncode == 0, f"Import script failed with exit code {res.returncode}.\nstdout: {res.stdout}\nstderr: {res.stderr}"

    # Verify the database count
    try:
        count_res = requests.get("http://localhost:8000/users/count", timeout=5).json()
    except Exception as e:
        pytest.fail(f"Failed to fetch user count from API after import: {e}")

    actual_count = count_res.get("count")
    assert actual_count == 5000, f"Expected 5000 users in the database, but got {actual_count}"

    # Assert metric threshold
    assert duration <= 12.0, f"Execution too slow: {duration:.2f} seconds (Threshold: <= 12.0s). Ensure you are using asynchronous I/O or a thread pool."