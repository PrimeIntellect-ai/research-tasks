# test_final_state.py
import os
import json
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/scripts/verify_backups.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_output_file_exists():
    output_path = "/home/user/output/valid_backup_pairs.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_output_file_contents():
    output_path = "/home/user/output/valid_backup_pairs.jsonl"

    expected_pairs = [
        {"database_id": "db_1", "storage_id": "stor_1"},
        {"database_id": "db_3", "storage_id": "stor_2"},
        {"database_id": "db_4", "storage_id": "stor_4"}
    ]

    actual_pairs = []
    with open(output_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
                # Check exact string format as required by the prompt, though json.loads handles semantics
                assert "database_id" in parsed and "storage_id" in parsed, f"Line {line_num} missing required keys."
                actual_pairs.append(parsed)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {output_path} is not valid JSON: {line}")

    assert len(actual_pairs) == len(expected_pairs), f"Expected {len(expected_pairs)} output lines, got {len(actual_pairs)}."

    # Check sorting by database_id
    db_ids = [p["database_id"] for p in actual_pairs]
    assert db_ids == sorted(db_ids), "Output is not sorted alphabetically by database_id."

    # Check exact match
    assert actual_pairs == expected_pairs, f"Output pairs do not match expected. Expected: {expected_pairs}, Got: {actual_pairs}"

    # Also verify the exact string format without spaces, as requested: '{"database_id":"<db_id>","storage_id":"<storage_id>"}'
    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        for expected, actual_line in zip(expected_pairs, lines):
            expected_str = f'{{"database_id":"{expected["database_id"]}","storage_id":"{expected["storage_id"]}"}}'
            # We allow standard json serialization which might have spaces, but the prompt says "exactly: ..."
            # So we strip spaces to be lenient on spacing but strict on keys/values
            actual_stripped = actual_line.replace(" ", "")
            expected_stripped = expected_str.replace(" ", "")
            assert actual_stripped == expected_stripped, f"Line format mismatch. Expected roughly {expected_str}, got {actual_line}"