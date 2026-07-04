# test_final_state.py

import os

def test_cleaned_data_exists_and_correct():
    file_path = "/home/user/cleaned_data.csv"

    # Check if the output file exists
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    expected_content = """1698825600,SENS-01,10.0,ALL CLEAR,10.00
1698825660,SENS-01,15.0,MINOR ISSUES,12.50
1698825720,SENS-01,20.0,ERROR 404,15.00
1698825780,SENS-01,10.0,FIXED,15.00
1698825840,SENS-01,12.0,OK,14.00"""

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Content of {file_path} does not match the expected final state.\nExpected:\n{expected_content}\n\nActual:\n{actual_content}"