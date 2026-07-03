# test_final_state.py

import os
import json
import sqlite3
import ctypes
import subprocess
import pytest

def test_shared_libraries_exist():
    libhwmock = "/home/user/project/lib/libhwmock.so"
    libmetrics = "/home/user/project/lib/libmetrics.so"

    assert os.path.isfile(libhwmock), f"Shared library missing: {libhwmock}"
    assert os.path.isfile(libmetrics), f"Shared library missing: {libmetrics}"

def test_libraries_loadable_and_linked():
    libhwmock_path = "/home/user/project/lib/libhwmock.so"
    libmetrics_path = "/home/user/project/lib/libmetrics.so"

    # Check if libmetrics is dynamically linked to libhwmock
    try:
        ldd_output = subprocess.check_output(["ldd", libmetrics_path], text=True)
        assert "libhwmock" in ldd_output, "libmetrics.so does not appear to be linked against libhwmock.so"
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ldd on libmetrics.so")

    # Load libhwmock first so libmetrics can resolve hw_init if rpath isn't set
    try:
        hwmock = ctypes.CDLL(libhwmock_path)
    except Exception as e:
        pytest.fail(f"Failed to load libhwmock.so: {e}")

    # Now load libmetrics
    try:
        metrics = ctypes.CDLL(libmetrics_path)
    except Exception as e:
        pytest.fail(f"Failed to load libmetrics.so: {e}")

    # Check function signature and return value
    metrics.get_system_score.restype = ctypes.c_double
    score = metrics.get_system_score()
    assert abs(score - 131.88) < 0.001, f"Expected get_system_score() to return ~131.88, got {score}"

def test_python_script_exists():
    script_path = "/home/user/project/test_metrics.py"
    assert os.path.isfile(script_path), f"Python script missing: {script_path}"

def test_database_schema_and_data():
    db_path = "/home/user/project/db/metrics.db"
    assert os.path.isfile(db_path), f"Database missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check schema
    cursor.execute("PRAGMA table_info(results);")
    columns = {info[1]: info[2] for info in cursor.fetchall()}
    assert "status" in columns, "Column 'status' was not added to the results table"
    assert columns["status"].upper() == "TEXT", f"Column 'status' should be of type TEXT, got {columns['status']}"

    # Check data
    cursor.execute("SELECT id, metric_name, metric_value, status FROM results ORDER BY id ASC;")
    rows = cursor.fetchall()

    assert len(rows) == 2, f"Expected 2 rows in results table, found {len(rows)}"

    # First row
    assert rows[0][1] == "baseline", "Row 1 metric_name should be 'baseline'"
    assert rows[0][2] == 100.0, "Row 1 metric_value should be 100.0"
    assert rows[0][3] is None, "Row 1 status should be NULL"

    # Second row
    assert rows[1][1] == "sys_score", "Row 2 metric_name should be 'sys_score'"
    assert abs(rows[1][2] - 131.88) < 0.001, "Row 2 metric_value should be ~131.88"
    assert rows[1][3] == "PASS", "Row 2 status should be 'PASS'"

    conn.close()

def test_output_json():
    output_path = "/home/user/output.json"
    assert os.path.isfile(output_path), f"Output JSON missing: {output_path}"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("output.json is not valid JSON")

    assert isinstance(data, list), "output.json should contain a JSON array"
    assert len(data) == 2, f"Expected 2 objects in output.json, found {len(data)}"

    # First object
    assert data[0].get("metric_name") == "baseline", "First object metric_name should be 'baseline'"
    assert data[0].get("metric_value") == 100.0, "First object metric_value should be 100.0"
    assert data[0].get("status") is None, "First object status should be null"

    # Second object
    assert data[1].get("metric_name") == "sys_score", "Second object metric_name should be 'sys_score'"
    assert abs(data[1].get("metric_value", 0) - 131.88) < 0.001, "Second object metric_value should be ~131.88"
    assert data[1].get("status") == "PASS", "Second object status should be 'PASS'"