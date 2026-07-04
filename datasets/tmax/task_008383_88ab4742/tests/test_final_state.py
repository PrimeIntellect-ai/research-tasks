# test_final_state.py

import os
import sqlite3
import json
import stat
import pytest

def test_builder_executable_exists():
    builder_path = "/home/user/legacy_builder/builder"
    assert os.path.exists(builder_path), f"The compiled executable {builder_path} does not exist."
    assert os.path.isfile(builder_path), f"{builder_path} is not a file."

    # Check if executable
    st = os.stat(builder_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"{builder_path} is not executable."

def test_database_schema_migrated():
    db_path = "/home/user/db/artifacts.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check that 'artifacts' table is dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='artifacts';")
    assert cursor.fetchone() is None, "The old 'artifacts' table was not dropped."

    # Check that 'artifacts_v2' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='artifacts_v2';")
    assert cursor.fetchone() is not None, "The new 'artifacts_v2' table does not exist."

    # Check columns of 'artifacts_v2'
    cursor.execute("PRAGMA table_info(artifacts_v2);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = {"id", "name", "size", "checksum", "status"}
    assert set(columns.keys()) == expected_columns, f"Expected columns {expected_columns}, but found {set(columns.keys())}."

    conn.close()

def test_final_artifacts_json_correct():
    json_path = "/home/user/final_artifacts.json"
    assert os.path.exists(json_path), f"The output JSON file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON data should be a list of objects."
    assert len(data) == 3, f"Expected 3 artifacts in the JSON output, found {len(data)}."

    # Sort data by id to ensure stable checking
    data_sorted = sorted(data, key=lambda x: x.get("id", 0))

    expected_data = [
        {
            "id": 1,
            "name": "legacy_core",
            "size": 45000,
            "checksum": None,
            "status": None
        },
        {
            "id": 2,
            "name": "service_alpha_bin",
            "size": 84500,
            "checksum": "a1b2c3d4e5",
            "status": "BUILT"
        },
        {
            "id": 3,
            "name": "service_beta_bin",
            "size": 128000,
            "checksum": "f6g7h8i9j0",
            "status": "BUILT"
        }
    ]

    for i, (actual, expected) in enumerate(zip(data_sorted, expected_data)):
        for key in expected:
            assert key in actual, f"Missing key '{key}' in artifact {i+1}."
            assert actual[key] == expected[key], f"Mismatch in artifact {i+1} for key '{key}': expected {expected[key]}, got {actual[key]}."