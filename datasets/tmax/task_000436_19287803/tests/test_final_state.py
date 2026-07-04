# test_final_state.py
import pytest
import requests
import sqlite3
import time

def test_database_indexes():
    """Verify that the student created appropriate indexes in the database."""
    conn = sqlite3.connect('/app/audit.db')
    c = conn.cursor()

    c.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index'")
    indexes = c.fetchall()

    # We expect at least an index on Employees(manager_id) and AccessLogs(timestamp) or similar
    # to satisfy the "optimize for recursive hierarchy queries and sorting by timestamps" requirement.
    index_tables = [idx[1] for idx in indexes]

    assert 'Employees' in index_tables, "No index created on the Employees table (expected for manager_id)."
    assert 'AccessLogs' in index_tables, "No index created on the AccessLogs table (expected for timestamp)."
    conn.close()

def test_api_manager_2_all_tampered():
    """Verify the API returns correctly sorted tampered logs for manager 2."""
    url = "http://127.0.0.1:8080/tampered?manager_id=2&page=1&limit=10"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "tampered_logs" in data, "Response missing 'tampered_logs' key."
    logs = data["tampered_logs"]

    # Manager 2 (Bob) and his subordinate 4 (David)
    # Tampered logs: 104 (David, ts 1600000400), 102 (Bob, ts 1600000200), 106 (Bob, ts 1600000150)
    expected_log_ids = [104, 102, 106]
    actual_log_ids = [log.get("log_id") for log in logs]

    assert actual_log_ids == expected_log_ids, f"Expected log IDs {expected_log_ids} in order, got {actual_log_ids}"

def test_api_manager_1_pagination():
    """Verify the API correctly paginates tampered logs for manager 1."""
    url = "http://127.0.0.1:8080/tampered?manager_id=1&page=2&limit=2"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "tampered_logs" in data, "Response missing 'tampered_logs' key."
    logs = data["tampered_logs"]

    # Manager 1 (Alice) hierarchy: everyone
    # Tampered logs total: 105 (ts 1600000500), 104 (ts 1600000400), 102 (ts 1600000200), 106 (ts 1600000150)
    # Page 2, Limit 2 means skipping the first 2 (105, 104) and returning the next 2 (102, 106)
    expected_log_ids = [102, 106]
    actual_log_ids = [log.get("log_id") for log in logs]

    assert actual_log_ids == expected_log_ids, f"Expected log IDs {expected_log_ids} for page 2, got {actual_log_ids}"

    # Also verify the structure of a single log
    if logs:
        log = logs[0]
        expected_keys = {"log_id", "emp_id", "res_id", "timestamp", "db_sig", "expected_sig"}
        assert expected_keys.issubset(log.keys()), f"Log entry missing expected keys. Found: {log.keys()}"
        assert log["log_id"] == 102
        assert log["db_sig"] == 99999
        assert log["expected_sig"] == (2 * 31) ^ (11 * 17) ^ (1600000200 % 100000), "Computed expected_sig is incorrect."

def test_api_empty_result():
    """Verify the API returns an empty array for a manager with no tampered logs or out of bounds page."""
    url = "http://127.0.0.1:8080/tampered?manager_id=1&page=10&limit=10"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()

    assert "tampered_logs" in data, "Response missing 'tampered_logs' key."
    assert data["tampered_logs"] == [], f"Expected empty array for tampered_logs, got {data['tampered_logs']}"