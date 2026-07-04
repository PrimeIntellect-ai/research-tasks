# test_final_state.py

import os
import pytest

def test_processed_sensor_data():
    file_path = "/home/user/processed_sensor.csv"

    # Check if the output file exists
    assert os.path.isfile(file_path), f"The output file {file_path} is missing."

    expected_content = """timestamp,rolling_avg
1600000000,10.00
1600000300,14.67
1600000600,20.00
1600000900,23.67
1600001200,18.00
1600001500,18.00
1600001800,24.67"""

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of {file_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )