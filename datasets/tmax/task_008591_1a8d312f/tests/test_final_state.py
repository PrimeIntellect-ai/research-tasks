# test_final_state.py
import os
import pytest

def test_cpp_source_exists():
    cpp_path = "/home/user/process_data.cpp"
    assert os.path.exists(cpp_path), f"The C++ source file {cpp_path} does not exist."
    assert os.path.isfile(cpp_path), f"{cpp_path} is not a file."

def test_executable_exists():
    exe_path = "/home/user/process_data"
    assert os.path.exists(exe_path), f"The compiled executable {exe_path} does not exist."
    assert os.path.isfile(exe_path), f"{exe_path} is not a file."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_processed_sensors_output():
    output_path = "/home/user/processed_sensors.csv"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    expected_lines = [
        "2023-10-12T14:35:00,0.3775",
        "2023-10-12T14:37:00,0.3900",
        "2023-10-12T14:38:00,1.0000",
        "2023-10-12T14:39:00,0.0000"
    ]

    with open(output_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    actual_lines = [line.strip() for line in actual_content.split('\n') if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_path}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}: expected '{expected}', but got '{actual}'."