# test_final_state.py

import os
import json
import subprocess
import pytest

def test_run_pipeline_success():
    """Verify run_pipeline.sh runs successfully with exit code 0."""
    script_path = "/home/user/legacy_pipeline/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} not found."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_pipeline.sh failed with exit code {result.returncode}.\nStderr: {result.stderr}"

def test_rejected_lines():
    """Verify rejected.txt contains exactly the two corrupted lines."""
    rejected_path = "/home/user/legacy_pipeline/data/rejected.txt"
    assert os.path.isfile(rejected_path), f"File {rejected_path} not found."

    with open(rejected_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        '{"id": 3, "name": "Charlie", "target_value": 300',
        '{"id": 5, "name": "Eve", "target_val: 500}'
    ]

    assert len(lines) == 2, f"Expected 2 rejected lines, found {len(lines)}."
    assert lines[0] == expected_lines[0], f"First rejected line mismatch. Expected: {expected_lines[0]}, Got: {lines[0]}"
    assert lines[1] == expected_lines[1], f"Second rejected line mismatch. Expected: {expected_lines[1]}, Got: {lines[1]}"

def test_output_jsonl():
    """Verify output.jsonl contains 4 JSON lines and Bob has final_value of 0."""
    output_path = "/home/user/legacy_pipeline/data/output.jsonl"
    assert os.path.isfile(output_path), f"File {output_path} not found."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 4, f"Expected 4 valid JSON lines in output.jsonl, found {len(lines)}."

    bob_found = False
    for line in lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in output.jsonl: {line}")

        if record.get("name") == "Bob":
            bob_found = True
            assert "final_value" in record, "Bob's record is missing 'final_value'."
            assert record["final_value"] == 0, f"Bob's final_value should be 0, got {record['final_value']}."

    assert bob_found, "Record for 'Bob' not found in output.jsonl."

def test_merged_timeline():
    """Verify merged_timeline.txt contains the exact chronological merged logs."""
    timeline_path = "/home/user/legacy_pipeline/logs/merged_timeline.txt"
    assert os.path.isfile(timeline_path), f"File {timeline_path} not found."

    expected_lines = [
        "2023-01-16T08:00:00Z Extracting batch 1",
        "2023-01-16T08:00:02Z Transformed batch 1",
        "2023-01-16T08:00:04Z Loaded batch 1",
        "2023-01-16T08:00:05Z Extracting batch 2",
        "2023-01-16T08:00:07Z Transformed batch 2",
        "2023-01-16T08:00:09Z Loaded batch 2"
    ]

    with open(timeline_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in timeline, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Timeline line {i+1} mismatch.\nExpected: {expected}\nGot: {actual}"