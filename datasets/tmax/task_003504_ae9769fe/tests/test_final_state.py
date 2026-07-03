# test_final_state.py

import os
import pytest

def test_clean_csv_exists_and_content():
    clean_csv_path = "/home/user/clean.csv"
    assert os.path.isfile(clean_csv_path), f"File {clean_csv_path} does not exist. The Go program may not have run or output to the wrong path."

    expected_content = """Time,Station,Metric,Value,RollAvg
1,Alpha,Hum,50.0,50.0
2,Alpha,Hum,52.0,51.0
3,Alpha,Hum,51.0,51.5
1,Alpha,Temp,20.0,20.0
2,Alpha,Temp,20.0,20.0
3,Alpha,Temp,24.0,22.0
1,Beta,Hum,0.0,0.0
2,Beta,Hum,60.0,30.0
1,Beta,Temp,15.0,15.0
2,Beta,Temp,16.0,15.5"""

    with open(clean_csv_path, "r") as f:
        content = f.read().strip()

    # Split lines and compare to handle potential CRLF/LF differences
    expected_lines = expected_content.splitlines()
    actual_lines = content.splitlines()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {clean_csv_path}, but found {len(actual_lines)}."

    for i, (expected_line, actual_line) in enumerate(zip(expected_lines, actual_lines)):
        assert actual_line == expected_line, f"Line {i+1} mismatch: expected '{expected_line}', got '{actual_line}'"