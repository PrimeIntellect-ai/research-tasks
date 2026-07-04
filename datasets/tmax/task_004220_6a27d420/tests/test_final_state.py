# test_final_state.py
import os
import pytest

def test_clean_logs_exists_and_content():
    """Check if /home/user/clean_logs.txt exists and has the correct cleaned content."""
    file_path = "/home/user/clean_logs.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected_lines = [
        "database connection failed due to timeout",
        "user authentication successful",
        "critical server overload detected impending crash",
        "warning high memory usage on server",
        "server crash reported by user",
        "disk space critical on server"
    ]

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        # Allow multiple spaces to be collapsed to single, as per instructions
        actual_normalized = " ".join(actual.split())
        assert actual_normalized == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual_normalized}'."

def test_jaccard_c_and_executable_exist():
    """Check if the C source file and compiled executable exist."""
    c_file = "/home/user/jaccard.c"
    exe_file = "/home/user/jaccard"

    assert os.path.isfile(c_file), f"C source file {c_file} does not exist."
    assert os.path.isfile(exe_file), f"Compiled executable {exe_file} does not exist."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_best_match_content():
    """Check if /home/user/best_match.txt contains the correct best match."""
    file_path = "/home/user/best_match.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected_match = "critical server overload detected impending crash"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    content_normalized = " ".join(content.split())
    assert content_normalized == expected_match, f"Content of {file_path} is incorrect. Expected '{expected_match}', got '{content_normalized}'."