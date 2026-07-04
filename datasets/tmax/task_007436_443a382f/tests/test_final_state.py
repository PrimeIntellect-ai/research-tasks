# test_final_state.py
import os
import sqlite3
import subprocess
import time
import json
import urllib.request
import urllib.error

def test_schema_migration():
    """Verify that the database schema was migrated correctly."""
    db_path = '/home/user/math_api/legacy.db'
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in c.fetchall()]

    assert 'old_formulas' not in tables, "Table 'old_formulas' was not dropped."
    assert 'expressions' in tables, "Table 'expressions' was not created."

    # Check columns of expressions table
    c.execute("PRAGMA table_info(expressions)")
    columns = {row[1] for row in c.fetchall()}
    expected_columns = {'id', 'name', 'expression', 'version'}
    assert expected_columns.issubset(columns), f"Table 'expressions' missing expected columns. Found: {columns}"

    # Check migrated data
    c.execute("SELECT name, expression FROM expressions WHERE name='kinetic_energy'")
    row = c.fetchone()
    assert row is not None, "Migrated data for 'kinetic_energy' not found."
    assert row[1] == '0.5 * m * v**2', f"Migrated data is incorrect. Expected '0.5 * m * v**2', got {row[1]}"

    conn.close()

def test_pytest_suite_passes():
    """Verify that the student's pytest suite passes."""
    test_file = '/home/user/math_api/test_app.py'
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."

    result = subprocess.run(['pytest', test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Pytest suite failed to pass:\n{result.stdout}\n{result.stderr}"

def test_api_evaluation():
    """Verify that the REST API evaluates expressions correctly."""
    app_file = '/home/user/math_api/app.py'
    assert os.path.isfile(app_file), f"API file {app_file} does not exist."

    server_process = subprocess.Popen(["python3", app_file])
    time.sleep(3) # Wait for server to start

    try:
        url = "http://127.0.0.1:5000/evaluate"
        payload = {
            "name": "kinetic_energy",
            "variables": {
                "m": 10.0,
                "v": 5.0
            }
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"API returned status {response.status}"
                response_body = response.read().decode('utf-8')
                response_data = json.loads(response_body)

                assert 'result' in response_data, "Response JSON missing 'result' key."
                assert abs(response_data['result'] - 125.0) < 0.001, f"Expected result ~125.0, got {response_data['result']}"
        except urllib.error.URLError as e:
            assert False, f"Failed to connect to API or API returned error: {e}"

    finally:
        server_process.terminate()
        server_process.wait(timeout=2)