# test_final_state.py
import os
import pytest

def test_executable_exists():
    assert os.path.isfile("/home/user/cleaner"), "/home/user/cleaner executable is missing."
    assert os.access("/home/user/cleaner", os.X_OK), "/home/user/cleaner is not executable."

def test_processed_data_content():
    assert os.path.isfile("/home/user/processed_data.csv"), "/home/user/processed_data.csv is missing."

    expected_lines = [
        "1620000001,120.50,-10.20,0",
        "1620000002,150.00,-50.00,1",
        "1620000003,150.00,15.00,0",
        "1620000004,150.00,15.00,0",
        "1620000006,140.00,0.00,2"
    ]

    with open("/home/user/processed_data.csv", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, "Processed data does not match the expected output format and rules."

def test_pipeline_script_exists():
    assert os.path.isfile("/home/user/pipeline_test.sh"), "/home/user/pipeline_test.sh is missing."
    assert os.access("/home/user/pipeline_test.sh", os.X_OK), "/home/user/pipeline_test.sh is not executable."

def test_test_result_log():
    assert os.path.isfile("/home/user/test_result.log"), "/home/user/test_result.log is missing."

    with open("/home/user/test_result.log", "r") as f:
        content = f.read().strip()

    assert content == "REPRODUCIBLE", f"Expected 'REPRODUCIBLE' in test_result.log, but got '{content}'"