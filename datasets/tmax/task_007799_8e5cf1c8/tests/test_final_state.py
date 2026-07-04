# test_final_state.py

import os
import pytest

def test_final_metrics_file_exists():
    file_path = "/home/user/final_metrics.txt"
    assert os.path.isfile(file_path), f"The output file {file_path} was not created."

def test_final_metrics_content():
    file_path = "/home/user/final_metrics.txt"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_string = "Average Latency: 68 ms"
    assert expected_string in content, f"Expected '{expected_string}' in {file_path}, but got:\n{content}"

def test_aggregate_executable_exists():
    exe_path = "/home/user/aggregator/aggregate"
    assert os.path.isfile(exe_path), f"The executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_cpp_source_exists():
    cpp_path = "/home/user/aggregator/aggregate.cpp"
    assert os.path.isfile(cpp_path), f"The source file {cpp_path} is missing."