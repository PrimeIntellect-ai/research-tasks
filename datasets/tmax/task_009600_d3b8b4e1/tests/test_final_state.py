# test_final_state.py

import os
import stat
import subprocess
import sqlite3
import pytest

SCRIPT_PATH = '/home/user/generate_audit_report.sh'
DB_PATH = '/home/user/audit.db'
CSV_PATH = '/home/user/violations.csv'

def test_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script at {SCRIPT_PATH} is not executable by the owner."

def test_script_execution_and_output():
    """Test that running the script produces the correct CSV output."""
    # Ensure previous runs don't interfere
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)

    # Execute the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute with return code {result.returncode}. stderr: {result.stderr}"

    # Check that the output file was created
    assert os.path.isfile(CSV_PATH), f"Output file not found at {CSV_PATH} after running the script."

    # Compute the expected result directly from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT e.name, d.name, a.system_name, a.access_time
        FROM access_logs a
        JOIN employees e ON a.employee_id = e.id
        JOIN departments d ON e.department_id = d.id
        JOIN system_clearances s ON a.system_name = s.system_name
        WHERE e.clearance_level < s.required_clearance
        ORDER BY a.access_time ASC
    """
    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_csv_lines = [",".join(map(str, row)) for row in expected_rows]

    # Read the actual output
    with open(CSV_PATH, 'r') as f:
        actual_content = f.read().strip()

    actual_csv_lines = [line.strip() for line in actual_content.split('\n') if line.strip()]

    # Compare actual vs expected
    assert actual_csv_lines == expected_csv_lines, (
        f"CSV content mismatch.\n"
        f"Expected:\n{chr(10).join(expected_csv_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_csv_lines)}"
    )