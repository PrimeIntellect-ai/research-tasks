# test_final_state.py
import os
import pytest

OUTPUT_FILE = '/home/user/critical_services.txt'

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"The output file {OUTPUT_FILE} was not found."
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a regular file."

def test_output_file_contents():
    expected_lines = [
        "user-db",
        "auth-service",
        "cache-redis"
    ]

    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {OUTPUT_FILE} do not match the expected output. "
        f"Expected: {expected_lines}, but got: {actual_lines}"
    )