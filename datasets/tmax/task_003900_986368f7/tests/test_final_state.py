# test_final_state.py

import os
import sys
import json
import sqlite3
import subprocess

SCRIPT_PATH = "/home/user/audit_query.py"
DB_PATH = "/home/user/audit.db"
REPORT_PATH = "/home/user/report.json"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_script_execution_and_output():
    # Clean up previous report if it exists
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    # Execute the script with the arguments specified in the verification process
    cmd = [
        sys.executable, SCRIPT_PATH,
        "--resource", "/etc/shadow",
        "--ip-prefix", "192.168.",
        "--limit", "2",
        "--offset", "1"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. Return code: {result.returncode}, stderr: {result.stderr}"

    assert os.path.exists(REPORT_PATH), f"Report file was not created at {REPORT_PATH} after script execution."

    with open(REPORT_PATH, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Report file {REPORT_PATH} does not contain valid JSON."

    assert isinstance(report_data, list), "Report JSON must be a JSON array (list) of objects."

    # Derive the expected data directly from the database to align with the truth
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT e.name, ac.resource, ac.access_timestamp, au.ip_address, au.auth_timestamp
    FROM employees e
    JOIN access_logs ac ON e.id = ac.emp_id
    JOIN auth_logs au ON e.id = au.emp_id
    WHERE e.department = 'Engineering'
      AND ac.resource = '/etc/shadow'
      AND au.ip_address LIKE '192.168.%'
    ORDER BY ac.access_timestamp DESC, au.auth_timestamp DESC, e.name ASC
    LIMIT 2 OFFSET 1
    """
    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_data = [dict(row) for row in expected_rows]

    assert len(report_data) == len(expected_data), f"Expected {len(expected_data)} records in the JSON report, but got {len(report_data)}."

    expected_keys = {"name", "resource", "access_timestamp", "ip_address", "auth_timestamp"}

    for i, (actual, expected) in enumerate(zip(report_data, expected_data)):
        actual_keys = set(actual.keys())
        assert actual_keys == expected_keys, f"Row {i} has incorrect keys. Expected {expected_keys}, got {actual_keys}"

        assert actual["name"] == expected["name"], f"Row {i}: Expected name '{expected['name']}', got '{actual['name']}'"
        assert actual["resource"] == expected["resource"], f"Row {i}: Expected resource '{expected['resource']}', got '{actual['resource']}'"
        assert actual["access_timestamp"] == expected["access_timestamp"], f"Row {i}: Expected access_timestamp '{expected['access_timestamp']}', got '{actual['access_timestamp']}'"
        assert actual["ip_address"] == expected["ip_address"], f"Row {i}: Expected ip_address '{expected['ip_address']}', got '{actual['ip_address']}'"
        assert actual["auth_timestamp"] == expected["auth_timestamp"], f"Row {i}: Expected auth_timestamp '{expected['auth_timestamp']}', got '{actual['auth_timestamp']}'"