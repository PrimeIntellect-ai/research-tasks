# test_final_state.py

import os
import pytest

def test_malicious_ips_output():
    output_file = "/home/user/malicious_ips.txt"
    assert os.path.isfile(output_file), f"The output file {output_file} was not generated."

    expected_lines = [
        "Detected SQL_INJECTION from 192.168.1.100",
        "Detected CROSS_SITE_SCRIPTING_XSS from 10.0.0.5",
        "Detected REMOTE_CODE_EXECUTION from 172.16.0.42"
    ]

    with open(output_file, "r") as f:
        content = f.read().strip().split('\n')

    # Remove any empty lines
    content = [line.strip() for line in content if line.strip()]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_file}, but found {len(content)}."

    for i, expected in enumerate(expected_lines):
        assert content[i] == expected, f"Line {i+1} mismatch: expected '{expected}', got '{content[i]}'."

def test_binary_exists():
    binary_file = "/home/user/parse_logs"
    assert os.path.isfile(binary_file), f"The compiled binary {binary_file} does not exist. Did you compile the C file?"
    assert os.access(binary_file, os.X_OK), f"The file {binary_file} is not executable."

def test_c_file_modified():
    c_file = "/home/user/parse_logs.c"
    assert os.path.isfile(c_file), f"The source file {c_file} is missing."

    with open(c_file, "r") as f:
        content = f.read()

    # The original file had `char token[16];`. To fix the bug, it should be modified,
    # or bounds checking added. We can't strictly assert the exact fix, but we can verify the output is correct.
    # However, checking that it's not the exact buggy line might be helpful, but the output test is the strongest.
    # We will just ensure the output file is correct as the primary verification.