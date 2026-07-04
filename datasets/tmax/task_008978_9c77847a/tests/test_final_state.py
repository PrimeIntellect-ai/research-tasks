# test_final_state.py
import os
import json
import pytest

def test_bad_commit_identified():
    expected_path = "/home/user/.expected_bad_commit"
    actual_path = "/home/user/bad_commit.txt"

    assert os.path.isfile(actual_path), f"File {actual_path} does not exist. You must write the bad commit SHA to this file."
    assert os.path.isfile(expected_path), f"Truth file {expected_path} is missing."

    with open(expected_path, 'r') as f:
        expected_commit = f.read().strip()

    with open(actual_path, 'r') as f:
        actual_commit = f.read().strip()

    assert actual_commit == expected_commit, f"Incorrect bad commit identified. Expected {expected_commit}, but got {actual_commit}."

def test_output_json_correct():
    output_path = "/home/user/output.json"

    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did you run the script successfully?"

    with open(output_path, 'r') as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} does not contain valid JSON.")

    expected_output = ["C", None, "3"]
    assert output_data == expected_output, f"Output JSON is incorrect or bug was not fixed properly. Expected {expected_output}, got {output_data}."