# test_final_state.py
import os
import subprocess
import pytest

def test_bad_commit_hash():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit_hash.txt"

    assert os.path.isfile(expected_file), f"Expected commit file {expected_file} is missing."
    assert os.path.isfile(actual_file), f"Student's commit file {actual_file} is missing."

    with open(expected_file, "r") as f:
        expected_commit = f.read().strip()

    with open(actual_file, "r") as f:
        actual_commit = f.read().strip()

    assert actual_commit == expected_commit, (
        f"Bad commit hash mismatch. Expected '{expected_commit}', got '{actual_commit}'."
    )

def test_fixed_output():
    input_file = "/home/user/data/input.txt"
    output_file = "/home/user/fixed_output.txt"

    assert os.path.isfile(input_file), f"Input file {input_file} is missing."
    assert os.path.isfile(output_file), f"Student's output file {output_file} is missing."

    # Compute expected output
    with open(input_file, "rb") as f:
        input_data = f.read()

    # The transformation is tr 'a' 'A'
    expected_output = input_data.replace(b'a', b'A')

    with open(output_file, "rb") as f:
        actual_output = f.read()

    assert actual_output == expected_output, (
        "The content of fixed_output.txt does not match the expected transformed data."
    )