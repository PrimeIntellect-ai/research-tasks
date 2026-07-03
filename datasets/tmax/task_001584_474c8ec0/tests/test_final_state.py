# test_final_state.py
import os

def test_result_file_exists():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist. Did you forget to write your answer?"

def test_correct_bad_commit():
    result_path = "/home/user/result.txt"
    expected_path = "/home/user/expected_bad_commit.txt"

    assert os.path.isfile(expected_path), f"Expected bad commit file {expected_path} is missing from the environment."
    assert os.path.isfile(result_path), f"Result file {result_path} is missing."

    with open(expected_path, "r") as f:
        expected_hash = f.read().strip()

    with open(result_path, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The commit hash in {result_path} ({actual_hash}) does not match the expected first bad commit ({expected_hash})."