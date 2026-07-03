# test_final_state.py

import os
import sqlite3
import json
import csv

DB_PATH = "/home/user/sensor_data.db"
JSON_PATH = "/home/user/correlated_sensors.json"
RAW_DATA_DIR = "/home/user/raw_data"

def test_db_exists_and_schema():
    """Test that the SQLite database exists and has the correct schema."""
    assert os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings';")
    table = cursor.fetchone()
    assert table is not None, "Table 'readings' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(readings);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = {"timestamp": "TEXT", "sensor_id": "TEXT", "value": "REAL"}
    for col, col_type in expected_columns.items():
        assert col in columns, f"Column '{col}' is missing from the 'readings' table."
        # SQLite types can be flexible, so we check if the expected type is in the actual type string
        assert expected_columns[col] in columns[col], f"Column '{col}' has incorrect type. Expected {expected_columns[col]}, got {columns[col]}."

    conn.close()

def test_db_row_count():
    """Test that the database contains the correct number of cleaned rows."""
    assert os.path.exists(RAW_DATA_DIR), f"Raw data directory not found at {RAW_DATA_DIR}"

    expected_count = 0
    for file_name in os.listdir(RAW_DATA_DIR):
        if file_name.endswith(".csv"):
            file_path = os.path.join(RAW_DATA_DIR, file_name)
            with open(file_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Drop rows where value is missing or sensor_id is empty
                    if row.get("value") and row.get("sensor_id"):
                        expected_count += 1

    assert os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM readings;")
    actual_count = cursor.fetchone()[0]
    conn.close()

    assert actual_count == expected_count, f"Expected {expected_count} rows in the database, but found {actual_count}."

def test_json_exists_and_valid():
    """Test that the JSON report exists and is valid JSON."""
    assert os.path.exists(JSON_PATH), f"JSON report not found at {JSON_PATH}"

    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {JSON_PATH} is not valid JSON.")

    assert isinstance(data, list), "JSON root must be a list."

def test_json_structure_and_content():
    """Test the structure, sorting, rounding, and specific content of the JSON report."""
    assert os.path.exists(JSON_PATH), f"JSON report not found at {JSON_PATH}"

    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    expected_keys = {"sensor_a", "sensor_b", "mean_corr", "ci_lower", "ci_upper"}

    for item in data:
        assert set(item.keys()) == expected_keys, f"JSON object has incorrect keys. Expected {expected_keys}, got {set(item.keys())}"
        assert item["sensor_a"] < item["sensor_b"], f"sensor_a ('{item['sensor_a']}') is not lexicographically smaller than sensor_b ('{item['sensor_b']}')."

        # Check rounding (3 decimal places)
        for key in ["mean_corr", "ci_lower", "ci_upper"]:
            val_str = str(item[key])
            if "." in val_str:
                decimals = len(val_str.split(".")[1])
                assert decimals <= 3, f"Value for {key} ({item[key]}) is not rounded to 3 decimal places."

    # Check sorting
    for i in range(len(data) - 1):
        pair1 = (data[i]["sensor_a"], data[i]["sensor_b"])
        pair2 = (data[i+1]["sensor_a"], data[i+1]["sensor_b"])
        assert pair1 <= pair2, "JSON list is not sorted by sensor_a, then sensor_b."

    # Check specific pairs that should be highly correlated
    pairs = {(d["sensor_a"], d["sensor_b"]) for d in data}
    expected_pairs = {("S_2", "S_7"), ("S_4", "S_9")}
    assert pairs == expected_pairs, f"Expected highly correlated pairs {expected_pairs}, but got {pairs}."

    # Check correlation directions
    for item in data:
        if item["sensor_a"] == "S_2" and item["sensor_b"] == "S_7":
            assert item["mean_corr"] > 0.9, f"Expected S_2 and S_7 to have strong positive correlation, got {item['mean_corr']}"
        elif item["sensor_a"] == "S_4" and item["sensor_b"] == "S_9":
            assert item["mean_corr"] < -0.9, f"Expected S_4 and S_9 to have strong negative correlation, got {item['mean_corr']}"