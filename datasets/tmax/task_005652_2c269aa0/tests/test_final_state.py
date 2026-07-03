# test_final_state.py
import os
import sqlite3
import csv

def test_extractor_executable_exists():
    exe_path = "/home/user/extractor"
    assert os.path.exists(exe_path), f"The compiled executable {exe_path} does not exist. Did you compile the C++ code?"
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_audit_report_csv_correctness():
    csv_path = "/home/user/audit_report.csv"
    assert os.path.exists(csv_path), f"The output file {csv_path} was not generated."

    db_path = "/home/user/audit.db"
    assert os.path.exists(db_path), f"The database file {db_path} is missing."

    # Compute expected results directly from the database to ensure correctness
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
        SELECT employees.name, employees.department, access_logs.resource, access_logs.timestamp
        FROM employees
        JOIN access_logs ON employees.id = access_logs.employee_id
        WHERE access_logs.status = 'DENIED'
        ORDER BY access_logs.timestamp DESC
        LIMIT 10;
    """
    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    # Read the generated CSV
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert len(actual_data) > 0, "The CSV file is empty."

    expected_header = ["Name", "Department", "Resource", "Timestamp"]
    assert actual_data[0] == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {actual_data[0]}"

    actual_rows = actual_data[1:]
    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but got {len(actual_rows)} rows."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        expected_str_list = [str(item) for item in expected]
        assert actual == expected_str_list, f"Row {i+1} mismatch.\nExpected: {expected_str_list}\nGot: {actual}"