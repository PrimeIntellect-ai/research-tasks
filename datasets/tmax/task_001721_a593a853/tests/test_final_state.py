# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_database_exists_and_schema():
    db_path = '/home/user/metrics.db'
    assert os.path.isfile(db_path), f"Database file not found at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='server_metrics'")
    table = cursor.fetchone()
    assert table is not None, "Table 'server_metrics' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(server_metrics)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    expected_columns = {
        'timestamp': 'TEXT',
        'latency_sec': 'REAL',
        'status': 'TEXT'
    }

    for col_name, col_type in expected_columns.items():
        assert col_name in columns, f"Column '{col_name}' is missing from 'server_metrics'."
        assert columns[col_name].upper() == col_type, f"Column '{col_name}' should be of type {col_type}, but got {columns[col_name]}."

    conn.close()

def test_database_content():
    db_path = '/home/user/metrics.db'
    assert os.path.isfile(db_path), f"Database file not found at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM server_metrics")
    count = cursor.fetchone()[0]
    assert count == 100, f"Expected 100 rows in 'server_metrics', found {count}."

    # Verify latency transformation
    cursor.execute("SELECT latency_sec, status FROM server_metrics")
    rows = cursor.fetchall()

    fails = sum(1 for row in rows if row[1] == 'FAIL')
    oks = sum(1 for row in rows if row[1] == 'OK')

    assert fails == 14, f"Expected 14 FAIL records in database, found {fails}."
    assert oks == 86, f"Expected 86 OK records in database, found {oks}."

    # Check a few latency values
    for latency, status in rows:
        if status == 'FAIL':
            assert abs(latency - 1.2) < 1e-5, f"Expected latency_sec for FAIL to be 1.2, got {latency}"
        elif status == 'OK':
            assert abs(latency - 0.15) < 1e-5, f"Expected latency_sec for OK to be 0.15, got {latency}"

    conn.close()

def test_infer_script_exists():
    script_path = '/home/user/infer.py'
    assert os.path.isfile(script_path), f"Python script not found at {script_path}"

def test_result_json():
    result_path = '/home/user/result.json'
    assert os.path.isfile(result_path), f"Result file not found at {result_path}"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} does not contain valid JSON.")

    assert 'posterior_mean' in data, "Key 'posterior_mean' is missing from the JSON output."

    posterior_mean = data['posterior_mean']
    assert isinstance(posterior_mean, (int, float)), "The value for 'posterior_mean' must be a number."

    expected_mean = 0.1429
    assert abs(posterior_mean - expected_mean) < 1e-5, f"Expected posterior_mean to be {expected_mean}, but got {posterior_mean}."