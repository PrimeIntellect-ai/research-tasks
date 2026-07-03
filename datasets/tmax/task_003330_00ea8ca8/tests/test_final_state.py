# test_final_state.py

import os
import pytest

def test_cleaned_sensors_csv_content():
    file_path = "/home/user/cleaned_sensors.csv"

    # Check if file exists
    assert os.path.exists(file_path), f"The output file {file_path} was not created."
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."

    expected_content = """bucket,sensor_id,avg_temp
2023-10-01T10:00:00Z,loc1,23.50
2023-10-01T10:00:00Z,loc2,24.00
2023-10-01T10:00:00Z,loc3,22.00
2023-10-01T11:00:00Z,loc1,20.50
2023-10-01T11:00:00Z,loc2,21.50
2023-10-01T11:00:00Z,loc3,19.50"""

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"The content of {file_path} does not match the expected output. Got:\n{actual_content}"

def test_go_script_exists():
    go_path = "/home/user/clean.go"
    assert os.path.exists(go_path), f"The Go program {go_path} was not created."
    assert os.path.isfile(go_path), f"{go_path} is not a regular file."