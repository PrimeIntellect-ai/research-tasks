# test_final_state.py

import os
import json
import pytest

def test_bad_commit_hash():
    user_file = "/home/user/bad_commit.txt"
    truth_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(user_file), f"File {user_file} does not exist."
    assert os.path.isfile(truth_file), f"Truth file {truth_file} does not exist."

    with open(user_file, 'r') as f:
        user_hash = f.read().strip()

    with open(truth_file, 'r') as f:
        truth_hash = f.read().strip()

    assert user_hash == truth_hash, f"Expected bad commit hash '{truth_hash}', but got '{user_hash}'."

def test_result_log_json():
    result_file = "/home/user/result.log"

    assert os.path.isfile(result_file), f"File {result_file} does not exist."

    with open(result_file, 'r') as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {result_file} is not valid JSON.")

    expected_data = {
        "name": "Bob",
        "age": "",
        "city": "London",
        "extra": "true"
    }

    assert data == expected_data, f"Expected JSON {expected_data}, but got {data}."