# test_final_state.py

import os
import json
import pytest

def test_scripts_exist():
    run_sh = "/home/user/run.sh"
    aggregator_go = "/home/user/aggregator.go"

    assert os.path.isfile(run_sh), f"Missing shell script at {run_sh}"
    assert os.access(run_sh, os.X_OK), f"Shell script at {run_sh} is not executable"
    assert os.path.isfile(aggregator_go), f"Missing Go program at {aggregator_go}"

def test_go_program_uses_flock():
    aggregator_go = "/home/user/aggregator.go"
    with open(aggregator_go, "r") as f:
        content = f.read()

    assert "syscall.Flock" in content, "Go program is missing syscall.Flock"
    assert "syscall.LOCK_EX" in content, "Go program is missing syscall.LOCK_EX"

def test_master_dataset_output():
    output_file = "/home/user/master_dataset.jsonl"
    assert os.path.isfile(output_file), f"Missing output file at {output_file}"

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    parsed_objects = []
    for i, line in enumerate(lines):
        try:
            parsed_objects.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {output_file} is not valid JSON: {line}")

    expected_objects = [
        {"id": "101", "measurement": "5.45", "timestamp": "2023-10-01T10:00:00Z"},
        {"id": "102", "measurement": "5.46", "timestamp": "2023-10-01T10:01:00Z"},
        {"id": "103", "measurement": "9.12", "timestamp": "2023-10-01T10:02:00Z"},
        {"id": "104", "measurement": "9.15", "timestamp": "2023-10-01T10:03:00Z"},
        {"id": "105", "measurement": "7.77", "timestamp": "2023-10-01T10:04:00Z"}
    ]

    assert len(parsed_objects) == len(expected_objects), \
        f"Expected {len(expected_objects)} JSON objects, but found {len(parsed_objects)} in {output_file}"

    # Sort both lists of dicts by 'id' to compare them deterministically
    parsed_objects_sorted = sorted(parsed_objects, key=lambda x: x.get("id", ""))
    expected_objects_sorted = sorted(expected_objects, key=lambda x: x["id"])

    assert parsed_objects_sorted == expected_objects_sorted, \
        f"Output data does not match the expected canonical output. Expected: {expected_objects_sorted}, Got: {parsed_objects_sorted}"