# test_final_state.py

import os
import pytest
import subprocess

def test_token_extracted():
    path = "/home/user/token.txt"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "aB9xQp2L5k99V", f"Incorrect token extracted. Got: {content}"

def test_mre_csv():
    path = "/home/user/mre.csv"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 1, f"Expected exactly one line in mre.csv, found {len(lines)}"
    parts = lines[0].split(",")
    assert len(parts) >= 3, "mre.csv line does not have enough columns"

    status = parts[2].strip()
    # The status should be empty or non-numeric to cause the original crash
    is_invalid = not status or not status.isdigit()
    assert is_invalid, f"mre.csv third column '{status}' is numeric, which would not cause the original script to crash"

def test_fixed_output():
    path = "/home/user/fixed_output.txt"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "OK: 101",
        "ERROR: 102 - not_found",
        "INVALID: 103",
        "ERROR: 104 - server_error"
    ]

    assert len(content) == len(expected), f"Expected {len(expected)} lines in fixed_output.txt, got {len(content)}"
    for i, (actual_line, expected_line) in enumerate(zip(content, expected)):
        assert actual_line.strip() == expected_line, f"Line {i+1} mismatch: expected '{expected_line}', got '{actual_line.strip()}'"

def test_legacy_processor_fixed():
    script_path = "/home/user/legacy_processor.sh"
    data_path = "/home/user/raw_data.csv"

    assert os.path.isfile(script_path), f"Missing file: {script_path}"
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable"

    # Run the script and check its output
    result = subprocess.run([script_path, data_path], capture_output=True, text=True)

    assert result.returncode == 0, f"Script failed with exit code {result.returncode}. Stderr: {result.stderr}"

    output_lines = result.stdout.strip().splitlines()
    expected = [
        "OK: 101",
        "ERROR: 102 - not_found",
        "INVALID: 103",
        "ERROR: 104 - server_error"
    ]

    assert len(output_lines) == len(expected), f"Expected {len(expected)} lines from script output, got {len(output_lines)}"
    for i, (actual_line, expected_line) in enumerate(zip(output_lines, expected)):
        assert actual_line.strip() == expected_line, f"Script output line {i+1} mismatch: expected '{expected_line}', got '{actual_line.strip()}'"