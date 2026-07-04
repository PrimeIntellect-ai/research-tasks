# test_final_state.py

import os
import json
import pytest

def test_output_file_exists():
    output_file = '/home/user/output.jsonl'
    assert os.path.isfile(output_file), f"Output file {output_file} is missing"

def test_output_contents():
    output_file = '/home/user/output.jsonl'
    assert os.path.isfile(output_file), f"Output file {output_file} is missing"

    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, "Output file is empty"

    records = []
    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
            records.append(record)
        except json.JSONDecodeError as e:
            pytest.fail(f"Line {i+1} is not valid JSON: {e}")

    # Check sorting
    ids = [rec.get("id") for rec in records]
    assert ids == sorted(ids), "Output records are not sorted alphabetically by 'id'"

    expected_results = {
        "A1": 0.000001,
        "B2": None,
        "C3": 1.0,
        "D4": 0.0
    }

    assert len(records) == len(expected_results), f"Expected {len(expected_results)} records, found {len(records)}"

    for rec in records:
        rec_id = rec.get("id")
        assert rec_id in expected_results, f"Unexpected id {rec_id} found in output"

        expected_std_dev = expected_results[rec_id]
        actual_std_dev = rec.get("std_dev")

        if expected_std_dev is None:
            assert actual_std_dev is None, f"Expected std_dev for {rec_id} to be null, got {actual_std_dev}"
        else:
            assert actual_std_dev is not None, f"Expected std_dev for {rec_id} to be a number, got null"
            assert isinstance(actual_std_dev, (int, float)), f"Expected std_dev for {rec_id} to be a number, got {type(actual_std_dev)}"
            diff = abs(actual_std_dev - expected_std_dev)
            assert diff <= 1e-5, f"std_dev for {rec_id} is incorrect. Expected ~{expected_std_dev}, got {actual_std_dev}"