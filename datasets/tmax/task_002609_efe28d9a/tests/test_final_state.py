# test_final_state.py

import os
import pytest

def test_bad_commit_identified_correctly():
    bad_commit_file = "/home/user/bad_commit.txt"
    secret_file = "/home/user/.secret_bad_commit"

    assert os.path.isfile(bad_commit_file), f"The file {bad_commit_file} was not created."
    assert os.path.isfile(secret_file), f"The secret verification file {secret_file} is missing."

    with open(secret_file, "r") as f:
        expected_hash = f.read().strip()

    with open(bad_commit_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, (
        f"The bad commit hash in {bad_commit_file} is incorrect.\n"
        f"Expected: {expected_hash}\n"
        f"Found: {actual_hash}"
    )

def test_expected_output_correct():
    expected_output_file = "/home/user/expected_output.txt"

    assert os.path.isfile(expected_output_file), f"The file {expected_output_file} was not created."

    with open(expected_output_file, "r") as f:
        actual_output = f.read().strip()

    expected_text = "Total Active: 320"

    assert actual_output == expected_text, (
        f"The output in {expected_output_file} is incorrect.\n"
        f"Expected: '{expected_text}'\n"
        f"Found: '{actual_output}'"
    )