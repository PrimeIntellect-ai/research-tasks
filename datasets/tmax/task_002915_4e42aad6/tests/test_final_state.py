# test_final_state.py
import os
import pytest

def test_output_csv_exists():
    csv_path = "/home/user/output.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} is missing."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

def test_output_csv_content():
    csv_path = "/home/user/output.csv"
    expected_content = """ts,sensor_id,value,rolling_avg
100,S1,10.0,10.0
105,S1,20.0,15.0
110,S1,30.0,25.0
100,S2,15.0,15.0
102,S2,25.0,20.0"""

    with open(csv_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {csv_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )