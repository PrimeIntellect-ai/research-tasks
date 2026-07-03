# test_final_state.py

import os
import json
import pytest

def test_output_json_exists():
    """Verify that the output.json file is created at the expected location."""
    file_path = '/home/user/output.json'
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

def test_output_json_contents():
    """Verify the contents of the output.json file match the expected ground truth."""
    file_path = '/home/user/output.json'

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    assert "dropped_features" in data, "Key 'dropped_features' is missing from the JSON output."
    assert "similar_to_1" in data, "Key 'similar_to_1' is missing from the JSON output."

    expected_dropped = ["flexibility"]
    expected_similar = [33, 41, 27]

    assert data["dropped_features"] == expected_dropped, \
        f"Expected dropped_features to be {expected_dropped}, but got {data['dropped_features']}."

    assert data["similar_to_1"] == expected_similar, \
        f"Expected similar_to_1 to be {expected_similar}, but got {data['similar_to_1']}."