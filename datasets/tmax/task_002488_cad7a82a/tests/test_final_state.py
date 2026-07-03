# test_final_state.py

import os
import subprocess

def test_cpp_source_exists():
    assert os.path.isfile("/home/user/validate_int.cpp"), "The C++ source file /home/user/validate_int.cpp is missing."

def test_executable_exists():
    executable_path = "/home/user/validate_int"
    assert os.path.isfile(executable_path), f"The executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_invalid_rows_output():
    output_path = "/home/user/invalid_rows.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} is missing."

    with open(output_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = ["4", "5", "6", "8", "11", "12"]

    assert content == expected_lines, (
        f"The contents of {output_path} do not match the expected invalid row numbers. "
        f"Expected: {expected_lines}, but got: {content}"
    )

def test_executable_behavior(tmp_path):
    # Create a dummy CSV to test the compiled executable
    dummy_csv = tmp_path / "dummy.csv"
    dummy_csv.write_text(
        "header1,header2\n"
        "1,10\n"
        "2,10.5\n"
        "3,-20\n"
        "4,NaN\n"
        "5,\n"
        "6,-\n"
        "7,abc\n"
    )

    executable_path = "/home/user/validate_int"
    if not os.path.isfile(executable_path) or not os.access(executable_path, os.X_OK):
        return # Skip if executable is missing, handled by test_executable_exists

    result = subprocess.run([executable_path, str(dummy_csv), "1"], capture_output=True, text=True)

    output_lines = result.stdout.strip().splitlines()
    expected_output = ["3", "5", "6", "7", "8"]

    assert output_lines == expected_output, (
        "The compiled executable did not produce the correct output on a test dataset. "
        f"Expected: {expected_output}, but got: {output_lines}"
    )