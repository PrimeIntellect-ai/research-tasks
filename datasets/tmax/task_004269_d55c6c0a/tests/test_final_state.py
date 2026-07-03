# test_final_state.py

import os
import pytest

def test_root_cause_file_exists():
    path = "/home/user/root_cause.txt"
    assert os.path.isfile(path), f"The file {path} does not exist. You must create it."

def test_root_cause_content():
    path = "/home/user/root_cause.txt"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Clean up the content: strip whitespace and convert to lower case
    cleaned_content = content.strip().lower()

    # The expected 2-byte sequence is 0x5C 0x00
    expected_content = "0x5c 0x00"

    assert cleaned_content == expected_content, (
        f"The content of {path} is incorrect. "
        f"Expected '{expected_content}', but got '{cleaned_content}'."
    )