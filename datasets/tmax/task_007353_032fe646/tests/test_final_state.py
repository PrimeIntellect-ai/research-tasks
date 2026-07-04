# test_final_state.py

import os
import pytest

def test_sanitize_c_exists():
    """Verify that the C source code file exists."""
    file_path = "/home/user/sanitize.c"
    assert os.path.isfile(file_path), f"C source file {file_path} is missing."

def test_sanitize_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    file_path = "/home/user/sanitize"
    assert os.path.isfile(file_path), f"Compiled executable {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_author_stats_csv():
    """Verify the final author_stats.csv has the correct content and formatting."""
    file_path = "/home/user/author_stats.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    expected_content = "asmith,2\nbwayne,1\ncjones,1\njdoe,2\n"

    with open(file_path, "r") as f:
        content = f.read()

    # Normalize line endings just in case, but require exact match
    content_normalized = content.replace("\r\n", "\n")
    if not content_normalized.endswith("\n"):
        content_normalized += "\n"

    assert content_normalized == expected_content, (
        f"Content of {file_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content_normalized}"
    )