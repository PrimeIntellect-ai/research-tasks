# test_final_state.py

import os
import pytest

def test_payload_file_exists():
    """Test that the payload.txt file has been created."""
    file_path = "/home/user/payload.txt"
    assert os.path.isfile(file_path), f"The expected output file {file_path} does not exist."

def test_payload_file_content():
    """Test that the payload.txt file contains the correct malicious URI."""
    file_path = "/home/user/payload.txt"
    expected_uri = "/?action=pay&token=1%27%3BDROP+TABLE+transactions%3B--"

    # Ensure the file exists before attempting to read it
    assert os.path.isfile(file_path), f"The expected output file {file_path} does not exist."

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == expected_uri, (
        f"The content of {file_path} is incorrect.\n"
        f"Expected: '{expected_uri}'\n"
        f"Got: '{content}'\n"
        "Make sure you extracted the full requested URI of the malicious packet."
    )