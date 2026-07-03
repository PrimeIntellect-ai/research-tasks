# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/find_paths.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_database_exists():
    db_path = "/home/user/graph.db"
    assert os.path.isfile(db_path), f"Database not found at {db_path}"

def test_reachable_txt_contents():
    output_path = "/home/user/reachable.txt"
    assert os.path.isfile(output_path), f"Output file not found at {output_path}"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "http://example.com/b",
        "http://example.com/c",
        "http://example.com/e"
    ]

    assert lines == expected_lines, f"Contents of {output_path} do not match the expected output. Got: {lines}"

def test_schema_txt_contents():
    schema_path = "/home/user/schema.txt"
    assert os.path.isfile(schema_path), f"Schema file not found at {schema_path}"

    with open(schema_path, "r") as f:
        content = f.read().upper()

    assert "CREATE INDEX" in content, f"No CREATE INDEX statements found in {schema_path}"