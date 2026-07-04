# test_final_state.py

import os
import json
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_pipeline_execution_and_output():
    script_path = "/home/user/run_pipeline.sh"
    output_path = "/home/user/clean_logs.jsonl"

    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    # Check if output file exists
    assert os.path.exists(output_path), f"Output file {output_path} was not created."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

    expected_records = [
        {"id": 1, "configs": {"timeout": "60", "retries": "3"}},
        {"id": 2, "configs": {"DB_PASSWORD": "***"}},
        {"id": 3, "configs": {"api_key": "***", "port": "8080"}},
        {"id": 4, "configs": {"auth_token": "***"}},
        {"id": 5, "configs": {}}
    ]

    actual_records = []
    with open(output_path, "r", encoding="utf-8") as f:
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
        f"Expected {len(expected_records)} records, but found {len(actual_records)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records), 1):
        assert "id" in actual, f"Record {i} is missing the 'id' key."
        assert "configs" in actual, f"Record {i} is missing the 'configs' key."
        assert actual["id"] == expected["id"], f"Record {i} id mismatch: expected {expected['id']}, got {actual['id']}."
        assert actual["configs"] == expected["configs"], (
            f"Record {i} configs mismatch: expected {expected['configs']}, got {actual['configs']}."
        )