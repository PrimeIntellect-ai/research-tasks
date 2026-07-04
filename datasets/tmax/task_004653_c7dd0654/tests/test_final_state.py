# test_final_state.py
import os
import pytest

def test_compromised_users_file_exists():
    output_path = "/home/user/compromised_users.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. The script did not generate the required file."

def test_compromised_users_content():
    output_path = "/home/user/compromised_users.txt"

    expected_lines = [
        "10.0.0.2,bob",
        "10.0.0.4,charlie",
        "10.0.0.5,dave"
    ]

    with open(output_path, "r") as f:
        # Read lines and strip any trailing whitespace/newlines
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} compromised users, but found {len(actual_lines)}."
    )

    for i, expected in enumerate(expected_lines):
        assert actual_lines[i] == expected, (
            f"Line {i+1} mismatch. Expected '{expected}', got '{actual_lines[i]}'."
        )