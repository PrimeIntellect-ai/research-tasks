# test_final_state.py

import os
import json
import pytest

def test_migrated_output_exists_and_correct():
    output_path = "/home/user/migrated_output.jsonl"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    expected_records = [
        {"transaction_id": 1001, "schema_version": 2, "properties": {"status": "success", "region": "us-east-1"}},
        {"transaction_id": 1002, "schema_version": 2, "properties": {"status": "failure", "error_code": "500", "retries": "3"}},
        {"transaction_id": 1003, "schema_version": 2, "properties": {}}
    ]

    actual_records = []
    with open(output_path, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError as e:
                pytest.fail(f"Line {line_num} in {output_path} is not valid JSON: {e}")

    assert len(actual_records) == len(expected_records), (
        f"Expected {len(expected_records)} records, but found {len(actual_records)} in {output_path}"
    )

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert actual == expected, f"Record {i+1} mismatch.\nExpected: {expected}\nActual: {actual}"

def test_setup_py_conditional_compilation():
    setup_path = "/home/user/log_processor/setup.py"
    assert os.path.isfile(setup_path), f"setup.py missing: {setup_path}"

    with open(setup_path, "r") as f:
        content = f.read()

    assert "ENABLE_C_EXT" in content, "setup.py does not check for ENABLE_C_EXT environment variable"

def test_run_pipeline_exists():
    pipeline_path = "/home/user/run_pipeline.py"
    assert os.path.isfile(pipeline_path), f"Pipeline script missing: {pipeline_path}"