# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    file_path = '/home/user/process_csv.c'
    assert os.path.isfile(file_path), f"C source file {file_path} is missing."

def test_c_executable_exists():
    file_path = '/home/user/process_csv'
    assert os.path.isfile(file_path), f"Compiled executable {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_metrics_csv_exists_and_content():
    file_path = '/home/user/output/metrics.csv'
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    expected_content = """emp_id,subordinate_count,dept_avg_salary,dept_salary_rank
1,3,78750.00,1
2,1,78750.00,2
3,0,78750.00,3
4,0,78750.00,4
5,3,93750.00,1
6,1,93750.00,3
7,0,93750.00,2
8,0,93750.00,4"""

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of {file_path} does not match the expected output. Got:\n{content}"