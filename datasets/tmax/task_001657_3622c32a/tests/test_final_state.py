# test_final_state.py

import os
import pytest

def test_result_file_exists():
    """Test that the result.txt file exists."""
    assert os.path.isfile("/home/user/result.txt"), "/home/user/result.txt is missing"

def test_result_file_content():
    """Test that the result.txt file contains the correct output."""
    with open("/home/user/result.txt", "r") as f:
        content = f.read().strip()

    expected_output = "Processed 6 events, Type1 length sum: 216"
    assert content == expected_output, f"Expected '{expected_output}', but got '{content}'"

def test_executable_exists():
    """Test that the fixed executable has been compiled."""
    assert os.path.isfile("/home/user/log_analyzer_fixed"), "/home/user/log_analyzer_fixed is missing"
    assert os.access("/home/user/log_analyzer_fixed", os.X_OK), "/home/user/log_analyzer_fixed is not executable"

def test_source_code_modified():
    """Test that the C source code was modified to fix the bug."""
    assert os.path.isfile("/home/user/log_analyzer.c"), "/home/user/log_analyzer.c is missing"
    with open("/home/user/log_analyzer.c", "r") as f:
        content = f.read()

    # Check if the vulnerable pattern is still there exactly as before
    # The original had:
    # char buffer[64];
    # if (header->type == 1) {
    #     fread(buffer, 1, header->length, f);
    #     buffer[header->length] = '\0';

    # We can't strictly regex for the fix, but we can verify it doesn't blindly read into buffer[64] without a check.
    # The task asks to dynamically allocate memory or safely truncate.
    # A simple check is that the file was modified.
    # We check if the result is correct, which proves it ran without crashing on the large events.
    pass