# test_final_state.py

import os
import pytest

def test_detect_deadlocks_c_exists():
    file_path = "/home/user/detect_deadlocks.c"
    assert os.path.isfile(file_path), f"The C source file {file_path} is missing."

def test_deadlocks_found_csv_exists_and_correct():
    file_path = "/home/user/deadlocks_found.csv"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing. Did you compile and run your program?"

    expected_content = """deadlocked_job_id
job_B
job_C
job_D
job_F
job_G
job_H
job_M
job_N
job_O
job_P"""

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"The content of {file_path} is incorrect. Expected:\n{expected_content}\n\nGot:\n{actual_content}"