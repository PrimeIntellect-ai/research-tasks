# test_final_state.py

import os
import json
import subprocess
import pytest

def test_recovered_tickets_jsonl():
    output_path = "/home/user/recovered_tickets.jsonl"
    assert os.path.isfile(output_path), f"{output_path} does not exist. Did you run the export command?"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 valid JSON lines in {output_path}, but found {len(lines)}"

    expected_records = [
        {"id": 1, "desc": "Login issue"},
        {"id": 2, "desc": "Mouse broken"},
        {"id": 3, "desc": "Server down"}
    ]

    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {output_path} is not valid JSON: {line}")

        assert record == expected_records[i], f"Record {i+1} mismatch. Expected {expected_records[i]}, got {record}"

def test_cargo_test_passes_and_includes_regression_test():
    project_dir = "/home/user/ticket-db"
    assert os.path.isdir(project_dir), f"{project_dir} does not exist"

    try:
        result = subprocess.run(
            ["cargo", "test"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"`cargo test` failed with exit code {e.returncode}. Output:\n{e.stdout}\n{e.stderr}")

    output = result.stdout + result.stderr
    assert "test_corrupted_wal_recovery" in output, "The test output does not mention `test_corrupted_wal_recovery`. Did you add the required test?"

def test_main_rs_modified():
    main_rs_path = "/home/user/ticket-db/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} does not exist"

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "test_corrupted_wal_recovery" in content, "The required test `test_corrupted_wal_recovery` is missing from main.rs"