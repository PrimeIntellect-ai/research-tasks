# test_final_state.py

import os

def test_verifier_c_exists():
    file_path = "/home/user/verifier.c"
    assert os.path.exists(file_path), f"Source file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_verifier_executable_exists():
    file_path = "/home/user/verifier"
    assert os.path.exists(file_path), f"Executable file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."
    assert os.access(file_path, os.X_OK), f"{file_path} is not executable."

def test_verification_out_exists():
    file_path = "/home/user/verification_out.txt"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_verification_out_content():
    file_path = "/home/user/verification_out.txt"

    expected_results = [
        "Job1: 4",
        "Job2: RATE_LIMIT",
        "Job3: 15",
        "Job4: ERROR",
        "Job5: 11",
        "Job6: ERROR",
        "Job7: 1"
    ]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_results), f"Expected {len(expected_results)} lines in {file_path}, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_results)):
        actual_normalized = actual.replace(" ", "")
        expected_normalized = expected.replace(" ", "")
        assert actual_normalized == expected_normalized, f"Mismatch on line {i+1}. Expected '{expected}', got '{actual}'."