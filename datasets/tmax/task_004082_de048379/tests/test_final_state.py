# test_final_state.py

import os

def test_bad_commit_found():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.exists(actual_file), f"File {actual_file} was not created. You must write the bad commit hash to this file."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The commit hash in {actual_file} is incorrect. Expected '{expected_hash}', but got '{actual_hash}'."