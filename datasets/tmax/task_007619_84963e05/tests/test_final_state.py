# test_final_state.py
import os
import sqlite3
import csv
import json
import pytest

def test_rust_project_exists():
    """Verify the Rust project directory and Cargo.toml exist."""
    project_dir = "/home/user/log_processor"
    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."
    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml missing in {project_dir}."

def test_processed_csv_content():
    """Verify the processed CSV file exists and contains the correctly transformed data."""
    csv_path = "/home/user/processed_logs.csv"
    assert os.path.isfile(csv_path), f"Processed CSV file {csv_path} is missing."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."
    headers = rows[0]
    assert headers == ["timestamp", "error_code", "message"], f"Incorrect CSV headers: {headers}"

    # Verify data against the original JSON
    json_path = "/home/user/logs.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)

    assert len(rows) - 1 == len(original_data), "Number of rows in CSV does not match JSON entries."

    for i, orig in enumerate(original_data):
        csv_row = rows[i + 1]
        assert str(orig["ts"]) == csv_row[0], f"Row {i+1}: timestamp mismatch."
        assert str(orig["code"]) == csv_row[1], f"Row {i+1}: error_code mismatch."
        assert orig["msg"].lower() == csv_row[2], f"Row {i+1}: message mismatch or not properly lowercased."

def test_sqlite_database_content():
    """Verify the SQLite database exists and contains the correct table and data."""
    db_path = "/home/user/analysis.db"
    assert os.path.isfile(db_path), f"SQLite database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='normalized_logs';")
    table = cursor.fetchone()
    assert table is not None, "Table 'normalized_logs' does not exist in the database."

    # Check data
    cursor.execute("SELECT timestamp, error_code, message FROM normalized_logs ORDER BY timestamp ASC;")
    rows = cursor.fetchall()

    json_path = "/home/user/logs.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
        # Sort original data by timestamp to match SQL ORDER BY
        original_data.sort(key=lambda x: x["ts"])

    assert len(rows) == len(original_data), "Number of rows in SQLite database does not match JSON entries."

    for i, orig in enumerate(original_data):
        db_row = rows[i]
        assert str(orig["ts"]) == str(db_row[0]), f"DB Row {i+1}: timestamp mismatch."
        assert str(orig["code"]) == str(db_row[1]), f"DB Row {i+1}: error_code mismatch."
        assert orig["msg"].lower() == db_row[2], f"DB Row {i+1}: message mismatch or not properly lowercased."

    conn.close()