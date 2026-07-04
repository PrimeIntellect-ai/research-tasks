# test_final_state.py

import os
import csv
import sqlite3
import pytest

def test_db_exists_and_data_imported():
    """Check that the database exists and contains the imported data."""
    db_path = "/home/user/sensor_data.db"
    assert os.path.isfile(db_path), f"Database file not found at {db_path}."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM readings")
        count = cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'readings' table: {e}")
    finally:
        conn.close()

    assert count == 10000, f"Expected 10000 rows in 'readings' table, found {count}."

def test_query_plan_optimal():
    """Check that the query plan uses an index and avoids a separate sorting pass."""
    plan_path = "/home/user/query_plan.txt"
    assert os.path.isfile(plan_path), f"Query plan file not found at {plan_path}."

    with open(plan_path, 'r') as f:
        content = f.read().upper()

    assert "USING INDEX" in content or "USING COVERING INDEX" in content, \
        "The query plan does not indicate that an index is being used."
    assert "TEMP B-TREE FOR ORDER BY" not in content and "B-TREE FOR ORDER BY" not in content, \
        "The query plan indicates a separate sorting pass (TEMP B-TREE FOR ORDER BY) is used, which is not optimal."

def test_exporter_files_exist():
    """Check that the C source code and compiled executable exist."""
    c_file = "/home/user/exporter.c"
    exe_file = "/home/user/exporter"

    assert os.path.isfile(c_file), f"C source file not found at {c_file}."
    assert os.path.isfile(exe_file), f"Compiled executable not found at {exe_file}."
    assert os.access(exe_file, os.X_OK), f"File at {exe_file} is not executable."

def test_anomalies_output():
    """Check that the anomalies.txt file contains the correct expected output."""
    csv_path = "/home/user/sensors.csv"
    out_path = "/home/user/anomalies.txt"

    assert os.path.isfile(csv_path), "Original CSV file missing."
    assert os.path.isfile(out_path), f"Output file not found at {out_path}."

    expected_records = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 5:
                continue
            ts = int(row[0])
            sensor = row[1]
            temp = float(row[2])
            status = row[4]

            if status == 'ERROR' and temp > 80.0:
                expected_records.append((ts, sensor, temp))

    # Sort by timestamp descending
    expected_records.sort(key=lambda x: x[0], reverse=True)

    expected_lines = [f"ALERT: [{rec[1]}] registered {rec[2]:.1f}C" for rec in expected_records]

    with open(out_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), \
        f"Expected {len(expected_lines)} lines in anomalies.txt, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}: expected '{expected}', got '{actual}'."