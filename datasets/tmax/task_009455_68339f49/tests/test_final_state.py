# test_final_state.py

import os

def test_bad_commit_hash_correct():
    actual_file = "/home/user/bad_commit_hash.txt"
    expected_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(actual_file), f"The file {actual_file} was not created."
    assert os.path.isfile(expected_file), f"The expected truth file {expected_file} is missing."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert expected_hash, "The expected hash is empty (setup issue)."
    assert actual_hash == expected_hash, (
        f"The commit hash in {actual_file} is incorrect. "
        f"Expected '{expected_hash}', but got '{actual_hash}'."
    )