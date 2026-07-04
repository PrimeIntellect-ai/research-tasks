# test_final_state.py

import os
import re

def test_executable_exists():
    executable_path = "/home/user/sensor_stats"
    assert os.path.isfile(executable_path), f"Executable not found at {executable_path}. Did you compile the C program?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_output_log_correct():
    output_path = "/home/user/output.log"
    assert os.path.isfile(output_path), f"Output file not found at {output_path}. Did you run the compiled program?"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_mean = "10000.300000"
    expected_variance = "0.020000"
    expected_stddev = "0.141421"

    assert f"Mean: {expected_mean}" in content, f"Expected Mean to be {expected_mean}, but got:\n{content}"
    assert f"Variance: {expected_variance}" in content, f"Expected Variance to be {expected_variance}, but got:\n{content}"
    assert f"StdDev: {expected_stddev}" in content, f"Expected StdDev to be {expected_stddev}, but got:\n{content}"

def test_source_code_modifications():
    source_path = "/home/user/sensor_stats.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

    with open(source_path, "r") as f:
        content = f.read()

    # Check that double is used instead of float
    assert "double" in content, "The source code does not seem to use 'double' precision types."