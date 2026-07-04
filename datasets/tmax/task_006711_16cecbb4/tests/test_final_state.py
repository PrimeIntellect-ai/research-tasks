# test_final_state.py

import os

def test_output_csv_exists_and_correct():
    output_path = "/home/user/output.csv"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

    expected_output = """sensor_id,timestamp,rolling_avg
1,1000,10.00
1,1005,11.00
1,1010,12.00
1,1025,14.00
1,1040,16.00
3,1020,5.00
3,1030,7.50
3,1035,10.00"""

    with open(output_path, "r") as f:
        actual_output = f.read().strip()

    expected_lines = expected_output.strip().splitlines()
    actual_lines = actual_output.strip().splitlines()

    assert len(actual_lines) == len(expected_lines), f"Output file has {len(actual_lines)} lines, expected {len(expected_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."

def test_cpp_source_exists():
    source_path = "/home/user/process.cpp"
    assert os.path.isfile(source_path), f"Expected C++ source file {source_path} does not exist."

def test_executable_exists():
    executable_path = "/home/user/process"
    assert os.path.isfile(executable_path), f"Expected executable file {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."