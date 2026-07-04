# test_final_state.py

import os
import json
import sqlite3
import pytest

NORMALIZED_DB_PATH = "/home/user/normalized_data.db"
SCHEMA_JSON_PATH = "/home/user/schema_validation.json"

def test_files_exist():
    """Test that the required output files were created."""
    assert os.path.isfile(NORMALIZED_DB_PATH), f"The normalized database file is missing at {NORMALIZED_DB_PATH}"
    assert os.path.isfile(SCHEMA_JSON_PATH), f"The schema validation JSON file is missing at {SCHEMA_JSON_PATH}"

def test_normalized_data_counts():
    """Test that the normalized tables contain the correct number of unique records."""
    conn = sqlite3.connect(NORMALIZED_DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM locations;")
        loc_count = cursor.fetchone()[0]
        assert loc_count == 2, f"Expected 2 locations, got {loc_count}"

        cursor.execute("SELECT COUNT(*) FROM sensors;")
        sensor_count = cursor.fetchone()[0]
        assert sensor_count == 2, f"Expected 2 sensors, got {sensor_count}"

        cursor.execute("SELECT COUNT(*) FROM readings;")
        reading_count = cursor.fetchone()[0]
        assert reading_count == 3, f"Expected 3 readings, got {reading_count}"
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query normalized tables: {e}")
    finally:
        conn.close()

def test_indexes_exist():
    """Test that the required indexes were created."""
    conn = sqlite3.connect(NORMALIZED_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_readings_loc_time';")
    idx_loc_time = cursor.fetchone()
    assert idx_loc_time is not None, "Missing index 'idx_readings_loc_time'"

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_readings_sensor';")
    idx_sensor = cursor.fetchone()
    assert idx_sensor is not None, "Missing index 'idx_readings_sensor'"

    conn.close()

def test_schema_validation_json():
    """Test that the schema validation JSON file is correctly formatted and contains table definitions."""
    with open(SCHEMA_JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("schema_validation.json is not a valid JSON file.")

    assert isinstance(data, list), "schema_validation.json should contain a JSON array."

    create_table_count = sum(1 for item in data if isinstance(item, str) and "CREATE TABLE" in item.upper())
    assert create_table_count >= 3, f"Expected at least 3 'CREATE TABLE' statements in JSON, found {create_table_count}"