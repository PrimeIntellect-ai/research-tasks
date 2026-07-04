# test_final_state.py

import os
import pytest

APP_DIR = "/home/user/telemetry_app"
FINAL_OUTPUT_FILE = os.path.join(APP_DIR, "final_count.txt")
BINARY_FILE = os.path.join(APP_DIR, "telemetry_processor")

def test_binary_exists():
    assert os.path.isfile(BINARY_FILE), f"Compiled binary {BINARY_FILE} does not exist. Did you compile the C program?"
    assert os.access(BINARY_FILE, os.X_OK), f"File {BINARY_FILE} is not executable."

def test_final_output_exists():
    assert os.path.isfile(FINAL_OUTPUT_FILE), f"Final output file {FINAL_OUTPUT_FILE} does not exist."

def test_final_output_content():
    assert os.path.isfile(FINAL_OUTPUT_FILE), f"Final output file {FINAL_OUTPUT_FILE} does not exist."
    with open(FINAL_OUTPUT_FILE, "r") as f:
        content = f.read().strip()

    expected_count = 50 * 100 # 50 files, 100 records each
    expected_string = f"Total records: {expected_count}"

    assert content == expected_string, f"Expected '{expected_string}', but found '{content}'. Check your C code fixes for race conditions, hangs, and crashes."