# test_final_state.py
import os
import re
import math

def test_result_file_exists():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Expected result file {result_path} is missing."

def test_result_content():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Expected result file {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    # Calculate expected values based on setup data
    # Group A scores: 10, 20, 30, 40
    scores = [10.0, 20.0, 30.0, 40.0]
    n = len(scores)
    mean = sum(scores) / n
    variance = sum((x - mean) ** 2 for x in scores) / (n - 1)
    std_dev = math.sqrt(variance)
    margin_of_error = 1.96 * (std_dev / math.sqrt(n))

    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error

    expected_string = f"Mean: {mean:.2f}, CI: [{lower_bound:.2f}, {upper_bound:.2f}]"

    assert content == expected_string, f"Content of {result_path} is incorrect. Expected '{expected_string}', got '{content}'."

def test_c_source_and_executable_exist():
    source_path = "/home/user/analyze.c"
    executable_path = "/home/user/analyze"

    assert os.path.isfile(source_path), f"C source file {source_path} is missing."
    assert os.path.isfile(executable_path), f"Executable file {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."