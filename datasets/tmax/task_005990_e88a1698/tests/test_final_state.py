# test_final_state.py

import os
import pytest

def test_clean_data_exists():
    """Test that the clean data file exists."""
    file_path = "/home/user/clean_data.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing. The C++ program did not produce the expected output file."
    assert os.path.isfile(file_path), f"{file_path} should be a file."

def test_clean_data_content():
    """Test that the clean data file contains the correct processed data."""
    file_path = "/home/user/clean_data.csv"
    expected_content = """record_id,masked_email,quarter,score
101,a***@company.com,Q1,85
101,a***@company.com,Q2,92
101,a***@company.com,Q3,95
101,a***@company.com,Q4,100
102,b***@domain.org,Q1,70
102,b***@domain.org,Q3,80
103,c***@startup.io,Q1,50
103,c***@startup.io,Q3,60
103,c***@startup.io,Q4,70
104,d***@enterprise.net,Q4,100
"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Compare stripped lines to ignore trailing newlines or extra spaces at the end of file
    actual_lines = [line.strip() for line in content.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines()]

    assert actual_lines == expected_lines, (
        f"Content of {file_path} does not match expected clean data.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{content}"
    )