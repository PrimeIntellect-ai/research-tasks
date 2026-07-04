# test_final_state.py

import os
import json

def test_c_program_exists():
    """Test that the C program was created."""
    assert os.path.isfile("/home/user/process_backups.c"), "The C program /home/user/process_backups.c is missing."

def test_json_output_exists():
    """Test that the JSON output file was generated."""
    assert os.path.isfile("/home/user/valid_backups.json"), "The output file /home/user/valid_backups.json is missing."

def test_json_output_content():
    """Test that the JSON output correctly filters and maps the valid backups."""
    json_path = "/home/user/valid_backups.json"

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"The file {json_path} does not contain valid JSON."

    assert isinstance(data, list), "The JSON output must be an array."

    # Expected valid rows based on the setup
    expected_records = [
        {"id": 1, "ts": 1690000000, "db": "users_db", "bytes": 1048576},
        {"id": 3, "ts": 1690000100, "db": "graph_db", "bytes": 2048},
        {"id": 6, "ts": 1690000300, "db": "analytics_db", "bytes": 999999}
    ]

    assert len(data) == len(expected_records), f"Expected {len(expected_records)} valid records in the JSON output, but found {len(data)}."

    expected_query = "INSERT INTO restored_backups (id, ts, db, bytes) VALUES (?, ?, ?, ?);"

    for i, (actual, expected) in enumerate(zip(data, expected_records)):
        assert "document" in actual, f"Record at index {i} is missing the 'document' key."
        doc = actual["document"]
        assert doc.get("id") == expected["id"], f"Record {i} 'id' mismatch. Expected {expected['id']}, got {doc.get('id')}."
        assert doc.get("ts") == expected["ts"], f"Record {i} 'ts' mismatch. Expected {expected['ts']}, got {doc.get('ts')}."
        assert doc.get("db") == expected["db"], f"Record {i} 'db' mismatch. Expected {expected['db']}, got {doc.get('db')}."
        assert doc.get("bytes") == expected["bytes"], f"Record {i} 'bytes' mismatch. Expected {expected['bytes']}, got {doc.get('bytes')}."

        assert "sql_param_query" in actual, f"Record at index {i} is missing the 'sql_param_query' key."
        assert actual["sql_param_query"] == expected_query, f"Record {i} 'sql_param_query' mismatch."

        assert "sql_bind_args" in actual, f"Record at index {i} is missing the 'sql_bind_args' key."
        bind_args = actual["sql_bind_args"]
        assert isinstance(bind_args, list), f"Record {i} 'sql_bind_args' must be a list."
        assert len(bind_args) == 4, f"Record {i} 'sql_bind_args' must have exactly 4 elements."

        expected_bind_args = [str(expected["id"]), str(expected["ts"]), expected["db"], str(expected["bytes"])]
        assert bind_args == expected_bind_args, f"Record {i} 'sql_bind_args' mismatch. Expected {expected_bind_args}, got {bind_args}."