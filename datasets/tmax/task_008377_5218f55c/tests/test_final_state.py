# test_final_state.py

import os
import pytest

def test_output_file_exists_and_content():
    output_file = "/home/user/output_data.csv"

    assert os.path.exists(output_file), f"Output file {output_file} is missing."
    assert os.path.isfile(output_file), f"Path {output_file} is not a file."

    expected_content = """timestamp,sensor_id,temperature,humidity,temp_roll_avg_3
100,S1,20.00,50.00,20.00
110,S1,20.00,51.00,20.00
120,S1,21.00,51.00,20.33
130,S1,21.00,51.00,20.67
100,S2,22.00,55.00,22.00
110,S2,22.50,55.00,22.25
120,S2,23.00,56.00,22.50
130,S2,23.50,57.00,23.00"""

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {output_file} does not match the expected output."

def test_executable_exists():
    executable = "/home/user/process"
    cpp_file = "/home/user/process_sensors.cpp"

    assert os.path.exists(cpp_file), f"C++ source file {cpp_file} is missing."
    assert os.path.exists(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."