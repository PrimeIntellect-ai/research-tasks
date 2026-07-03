# test_final_state.py
import os

def test_bad_commit():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.exists(expected_file), f"Truth file {expected_file} is missing."
    assert os.path.exists(actual_file), f"Student output file {actual_file} is missing."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Incorrect bad commit hash. Expected '{expected_hash}', got '{actual_hash}'."

def test_result():
    actual_file = "/home/user/result.txt"
    assert os.path.exists(actual_file), f"Student output file {actual_file} is missing."

    with open(actual_file, "r") as f:
        actual_result = f.read().strip()

    expected_result = "333332833333500000"
    assert actual_result == expected_result, f"Incorrect math result. Expected '{expected_result}', got '{actual_result}'."

def test_secret():
    actual_file = "/home/user/secret.txt"
    assert os.path.exists(actual_file), f"Student output file {actual_file} is missing."

    with open(actual_file, "r") as f:
        actual_secret = f.read().strip()

    expected_secret = "X89B-SECR-9921"
    assert actual_secret == expected_secret, f"Incorrect API key secret. Expected '{expected_secret}', got '{actual_secret}'."