# test_final_state.py

import os
import re
import pytest

def test_tar_slip_prevented():
    """Verify that the system_state.json file was not overwritten by a tar slip attack."""
    state_file = "/home/user/system_state.json"
    assert os.path.exists(state_file), f"Critical file {state_file} is missing!"

    with open(state_file, "r") as f:
        content = f.read().strip()

    assert content == "SECURE_STATE", (
        f"Tar slip attack succeeded or file tampered with! "
        f"Expected 'SECURE_STATE', got '{content}'"
    )

def test_csv_files_exist_and_correct():
    """Verify that the processed logs exist in the correct location and contain the correct CSV data."""
    processed_dir = "/home/user/processed_logs"

    expected_files = {
        "log_0001.csv": [
            "Timestamp,EventID,Severity,Payload",
            "1600000000,10,1,System start",
            "1600000005,12,2,Warning temp"
        ],
        "log_0002.csv": [
            "Timestamp,EventID,Severity,Payload",
            "1600000010,15,0,All good"
        ],
        "log_0003.csv": [
            "Timestamp,EventID,Severity,Payload",
            "1600000020,99,3,Fatal error"
        ]
    }

    for filename, expected_lines in expected_files.items():
        file_path = os.path.join(processed_dir, filename)
        assert os.path.exists(file_path), f"Missing expected CSV file: {file_path}"

        with open(file_path, "r") as f:
            content = f.read().strip()

        # Check that all expected lines are present in the file
        for line in expected_lines:
            assert line in content, f"Expected record '{line}' not found in {file_path}"

        # Check header
        assert content.startswith("Timestamp,EventID,Severity,Payload"), (
            f"CSV {file_path} does not start with the correct header."
        )

def test_c_program_exists_and_uses_atomic_writes():
    """Verify that the C program exists and implements atomic writes using rename()."""
    c_code_path = "/home/user/convert_logs.c"
    assert os.path.exists(c_code_path), f"C source code not found at {c_code_path}"

    with open(c_code_path, "r") as f:
        code = f.read()

    # Check for rename() usage
    assert re.search(r'\brename\s*\(', code), (
        "The C program does not appear to use the POSIX rename() function "
        "required for atomic writes."
    )