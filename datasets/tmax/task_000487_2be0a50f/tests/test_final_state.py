# test_final_state.py

import os
import json
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_graph.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_output_file_exists():
    output_path = "/home/user/circular_citations.jsonl"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

def test_output_file_content():
    output_path = "/home/user/circular_citations.jsonl"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    expected_data = [
        {"cycle_id": "P1-P2-P3", "authors": ["Alice Adams", "Bob Baker", "Charlie Clark"]},
        {"cycle_id": "P4-P5-P6", "authors": ["Diana Doe", "Evan Evans", "Fiona Fox"]}
    ]

    actual_data = []
    with open(output_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                actual_data.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON line in output: {line}")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} cycles, found {len(actual_data)}"

    # Sort actual data by cycle_id to ensure deterministic comparison
    actual_data_sorted = sorted(actual_data, key=lambda x: x.get("cycle_id", ""))
    expected_data_sorted = sorted(expected_data, key=lambda x: x["cycle_id"])

    for actual, expected in zip(actual_data_sorted, expected_data_sorted):
        assert "cycle_id" in actual, "Missing 'cycle_id' in JSON object"
        assert "authors" in actual, "Missing 'authors' in JSON object"

        assert actual["cycle_id"] == expected["cycle_id"], f"Expected cycle_id {expected['cycle_id']}, got {actual['cycle_id']}"

        # Authors should be sorted alphabetically as per requirements
        assert isinstance(actual["authors"], list), "'authors' must be a list"
        assert actual["authors"] == sorted(actual["authors"]), f"Authors list is not sorted alphabetically: {actual['authors']}"
        assert actual["authors"] == expected["authors"], f"Expected authors {expected['authors']}, got {actual['authors']}"