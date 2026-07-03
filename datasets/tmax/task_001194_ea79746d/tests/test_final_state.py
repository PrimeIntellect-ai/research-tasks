# test_final_state.py

import os
import json
import pytest

def test_manifest_sorted_exists_and_correct():
    """Test that manifest_sorted.jsonl exists and contains the correct JSON objects in order."""
    manifest_path = '/home/user/manifest_sorted.jsonl'

    assert os.path.exists(manifest_path), f"The file {manifest_path} does not exist."
    assert os.path.isfile(manifest_path), f"The path {manifest_path} is not a file."

    expected_data = [
        {"filename": "alpha.dat", "id": 101, "timestamp": "2023-01-01T00:00:00Z"},
        {"filename": "beta.dat", "id": 102, "timestamp": "2023-01-02T00:00:00Z"},
        {"filename": "gamma.dat", "id": 103, "timestamp": "2023-01-03T00:00:00Z"}
    ]

    actual_data = []
    with open(manifest_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                actual_data.append(json.loads(line))
            except json.JSONDecodeError as e:
                pytest.fail(f"Failed to parse JSON line in {manifest_path}: {line}\nError: {e}")

    assert len(actual_data) == len(expected_data), (
        f"Expected {len(expected_data)} lines in {manifest_path}, but found {len(actual_data)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, (
            f"Line {i+1} in {manifest_path} does not match expected.\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}"
        )