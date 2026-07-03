# test_final_state.py

import os
import json
import pytest

def test_recovered_lineage_file_exists():
    """Check if the recovered_lineage.json file was generated."""
    filepath = "/home/user/experiments/recovered_lineage.json"
    assert os.path.isfile(filepath), f"Expected output file {filepath} is missing. The Rust program may not have been run or failed to output to the correct path."

def test_recovered_lineage_content():
    """Check if the recovered_lineage.json contains the correct matches in the correct order."""
    filepath = "/home/user/experiments/recovered_lineage.json"
    assert os.path.isfile(filepath), f"Expected output file {filepath} is missing."

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} does not contain valid JSON.")

    expected_data = [
        {
            "id": "data_1",
            "artifact_id": "artifact_alpha"
        },
        {
            "id": "data_2",
            "artifact_id": "artifact_beta"
        },
        {
            "id": "data_3",
            "artifact_id": "artifact_gamma"
        }
    ]

    assert isinstance(data, list), f"Expected the root JSON element to be a list, but got {type(data).__name__}."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in the JSON array, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a dictionary."
        assert "id" in actual, f"Item at index {i} is missing the 'id' key."
        assert "artifact_id" in actual, f"Item at index {i} is missing the 'artifact_id' key."

        assert actual["id"] == expected["id"], f"Expected id '{expected['id']}' at index {i}, but got '{actual['id']}'."
        assert actual["artifact_id"] == expected["artifact_id"], f"Expected artifact_id '{expected['artifact_id']}' for id '{actual['id']}', but got '{actual['artifact_id']}'."