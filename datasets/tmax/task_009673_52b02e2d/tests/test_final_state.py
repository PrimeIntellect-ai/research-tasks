# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_optimize_sql_exists_and_content():
    """Verify that optimize.sql exists and contains a CREATE INDEX statement for logs."""
    sql_path = "/home/user/optimize.sql"
    assert os.path.exists(sql_path), f"SQL script {sql_path} does not exist."

    with open(sql_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    assert "create " in content and "index " in content, f"{sql_path} must contain a CREATE INDEX statement."
    assert "logs" in content, f"{sql_path} must reference the 'logs' table."
    assert "device_id" in content, f"{sql_path} must reference the 'device_id' column."

def test_index_applied_to_db():
    """Verify that an index was actually created on the logs table in the SQLite database."""
    db_path = "/home/user/data/telemetry.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='logs';")
    indices = cursor.fetchall()
    conn.close()

    assert len(indices) > 0, "No index was found on the 'logs' table. Did you execute the SQL script?"

def test_rust_project_exists():
    """Verify that a Rust project was initialized at the expected location."""
    cargo_path = "/home/user/etl_processor/Cargo.toml"
    assert os.path.exists(cargo_path), f"Rust project not found: {cargo_path} does not exist."

def test_region_summary_json():
    """Verify that the region_summary.json output file exists and contains the correct maximum temperatures."""
    json_path = "/home/user/region_summary.json"
    assert os.path.exists(json_path), f"Output file {json_path} does not exist."

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    expected_data = {
        "North": 20.0,
        "South": 30.1,
        "East": 22.0,
        "West": 25.5
    }

    assert isinstance(data, dict), f"Expected the JSON output to be an object/dict, got {type(data).__name__}."

    for region, expected_temp in expected_data.items():
        assert region in data, f"Region '{region}' is missing from the output JSON."
        actual_temp = data[region]
        assert isinstance(actual_temp, (int, float)), f"Value for '{region}' must be a number, got {type(actual_temp).__name__}."
        assert abs(actual_temp - expected_temp) < 1e-5, f"Expected max temperature for {region} to be {expected_temp}, but got {actual_temp}."