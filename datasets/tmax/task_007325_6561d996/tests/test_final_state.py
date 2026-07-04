# test_final_state.py

import os
import pytest

def test_c_source_and_executable_exist():
    source_path = "/home/user/process.c"
    executable_path = "/home/user/process"

    assert os.path.isfile(source_path), f"C source code {source_path} is missing."
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_processed_output():
    output_path = "/home/user/processed.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    expected_lines = [
        "user_id|masked_email|type|norm_score|tokens",
        "101|jo***@test.com|A|0.50|good_job",
        "101|jo***@test.com|B|0.75|needs_work",
        "102|ja***@test.com|A|0.90|excellent",
        "103|a***@domain.org|B|0.10|very_bad"
    ]

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {output_path} is incorrect. Expected: {expected_lines}, but got: {actual_lines}"

def test_process_log():
    log_path = "/home/user/process.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    expected_lines = [
        "LOG: Processed line 1",
        "LOG: Processed line 2",
        "LOG: Processed line 3"
    ]

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {log_path} is incorrect. Expected: {expected_lines}, but got: {actual_lines}"