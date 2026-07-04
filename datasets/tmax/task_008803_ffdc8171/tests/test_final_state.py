# test_final_state.py
import os
import re

def test_process_logs_sh_executable():
    path = "/home/user/process_logs.sh"
    assert os.path.exists(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

def test_imputer_c_exists():
    path = "/home/user/imputer.c"
    assert os.path.exists(path), f"C program {path} does not exist."

def test_clean_logs_csv():
    path = "/home/user/clean_logs.csv"
    assert os.path.exists(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1620000000,SENS-ABC-1234,22.5,200",
        "1620000010,SENS-ABC-1234,22.5,200",
        "1620000040,SENS-XYZ-9876,22.5,500",
        "1620000050,SENS-XYZ-9876,25.1,404",
        "1620000070,SENS-QWE-5555,25.1,200"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch in {path}. Expected '{expected}', got '{actual}'."

def test_pipeline_log():
    path = "/home/user/pipeline.log"
    assert os.path.exists(path), f"Log file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"{path} is empty."

    last_line = lines[-1]
    expected_log = "Discarded: 2, Imputed: 3"
    assert last_line == expected_log, f"Expected last line of {path} to be '{expected_log}', got '{last_line}'."