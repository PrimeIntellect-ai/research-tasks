# test_final_state.py

import os
import pytest

def test_c_source_code_exists():
    """Check if the C source code file was created."""
    file_path = "/home/user/cleaner.c"
    assert os.path.isfile(file_path), f"C source code file {file_path} is missing."

def test_c_executable_exists():
    """Check if the C program was compiled to the correct location."""
    file_path = "/home/user/cleaner"
    assert os.path.isfile(file_path), f"Compiled executable {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_cleaned_long_csv_exists():
    """Check if the output CSV file was generated."""
    file_path = "/home/user/data/cleaned_long.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

def test_cleaned_long_csv_content():
    """Check if the output CSV file contains the correctly cleaned and reshaped data."""
    output_path = "/home/user/data/cleaned_long.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        actual_content = f.read().strip()

    expected_content = """timestamp,sensor_type,value
1620000000,temp,22.50
1620000000,humidity,0.00
1620000000,pressure,1013.20
1620000005,temp,23.00
1620000005,humidity,45.20
1620000005,pressure,1012.50
1620000010,temp,21.50
1620000010,humidity,44.00
1620000010,pressure,1011.00
1620000015,temp,0.00
1620000015,humidity,0.00
1620000015,pressure,1010.10"""

    assert actual_content == expected_content, f"Content of {output_path} does not match the expected final state."