# test_final_state.py

import os
import subprocess
import pytest

def test_final_state():
    script_path = "/home/user/build_and_test.sh"
    calc_path = "/home/user/calc"
    math_result_path = "/home/user/math_result.txt"

    # 1. Verify script exists and is executable
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # 2. Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # 3. Verify calc executable exists
    assert os.path.isfile(calc_path), f"Executable {calc_path} was not created."
    assert os.access(calc_path, os.X_OK), f"File {calc_path} is not executable."

    # 4. Verify calc exits with 73
    calc_result = subprocess.run([calc_path])
    assert calc_result.returncode == 73, f"Expected {calc_path} to exit with 73, but got {calc_result.returncode}."

    # 5. Calculate expected sum from the generated binary
    with open(calc_path, "rb") as f:
        binary_data = f.read()

    hex_str = binary_data.hex()
    expected_sum = sum(int(char) for char in hex_str if char.isdigit())

    # 6. Verify math_result.txt
    assert os.path.isfile(math_result_path), f"Result file {math_result_path} was not created."

    with open(math_result_path, "r") as f:
        actual_sum_str = f.read().strip()

    assert actual_sum_str.isdigit(), f"Result file {math_result_path} does not contain a valid integer: '{actual_sum_str}'"
    actual_sum = int(actual_sum_str)

    assert actual_sum == expected_sum, f"Expected sum {expected_sum}, but got {actual_sum} in {math_result_path}."