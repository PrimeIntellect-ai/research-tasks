# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/telemetry.db"
C_FILE_PATH = "/home/user/etl_extract.c"
JSON_OUT_PATH = "/home/user/extract.json"

def test_index_created():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_status_time';")
    row = cursor.fetchone()
    conn.close()
    assert row is not None, "Index 'idx_status_time' does not exist in the database."

def test_c_program_uses_bindings():
    assert os.path.exists(C_FILE_PATH), f"C source file {C_FILE_PATH} is missing."
    with open(C_FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    bind_count = content.count("sqlite3_bind_")
    assert bind_count >= 3, (
        f"Expected at least 3 sqlite3_bind_* calls in {C_FILE_PATH} to prevent SQL injection, "
        f"but found {bind_count}."
    )

def test_json_output_correct():
    assert os.path.exists(JSON_OUT_PATH), f"Output file {JSON_OUT_PATH} is missing. Did the program run successfully?"

    with open(JSON_OUT_PATH, 'r', encoding='utf-8') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {JSON_OUT_PATH} as JSON: {e}")

    assert isinstance(actual_data, list), "The JSON output should be a list of objects."

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, sensor_id, timestamp, reading 
        FROM sensor_data 
        WHERE status = ? 
        ORDER BY timestamp DESC 
        LIMIT ? OFFSET ?
    ''', ("ERROR", 5, 10))

    expected_data = []
    for r in cursor.fetchall():
        expected_data.append({
            "id": r["id"],
            "sensor_id": r["sensor_id"],
            "timestamp": r["timestamp"],
            "reading": r["reading"]
        })
    conn.close()

    assert actual_data == expected_data, (
        f"JSON data in {JSON_OUT_PATH} does not match expected output.\n"
        f"Expected: {expected_data}\n"
        f"Actual: {actual_data}"
    )