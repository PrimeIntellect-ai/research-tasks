# test_final_state.py
import os
import pytest

def test_validator_cpp_exists():
    path = "/home/user/rate_limiter/validator.cpp"
    assert os.path.isfile(path), f"File {path} is missing. Did you create validator.cpp?"

def test_server_bin_exists_and_executable():
    bin_path = "/home/user/rate_limiter/server_bin"
    assert os.path.isfile(bin_path), f"Executable {bin_path} is missing. Did you compile the code?"
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_results_txt_contents():
    results_path = "/home/user/rate_limiter/results.txt"
    assert os.path.isfile(results_path), f"File {results_path} is missing. Did you run the executable?"

    expected_lines = [
        "ACCEPTED",
        "ACCEPTED",
        "ACCEPTED",
        "LIMITED",
        "INVALID",
        "ACCEPTED",
        "ACCEPTED",
        "INVALID",
        "INVALID",
        "INVALID"
    ]

    with open(results_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {results_path} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual:   {actual_lines}"
    )