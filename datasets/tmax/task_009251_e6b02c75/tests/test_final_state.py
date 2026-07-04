# test_final_state.py

import os
import re

def test_c_source_exists():
    assert os.path.isfile("/home/user/cleaner.c"), "The C source file /home/user/cleaner.c does not exist."

def test_executable_exists():
    assert os.path.isfile("/home/user/cleaner"), "The compiled executable /home/user/cleaner does not exist."
    assert os.access("/home/user/cleaner", os.X_OK), "The file /home/user/cleaner is not executable."

def test_output_file_exists():
    assert os.path.isfile("/home/user/cleaned_feedback.txt"), "The output file /home/user/cleaned_feedback.txt does not exist."

def test_output_file_content():
    expected_lines = [
        "1670000000|U001|***@example.com|great service highly recommend",
        "1670000005|U002|***@work.net|terrible just terrible",
        "1670000010|U003|***@domain.org|okay experience",
        "1670000020|U005|***@test.com|i loved it"
    ]

    with open("/home/user/cleaned_feedback.txt", "r") as f:
        content = f.read().strip().split('\n')

    # Remove any empty lines that might have been accidentally added
    content = [line.strip() for line in content if line.strip()]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in output, but got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"