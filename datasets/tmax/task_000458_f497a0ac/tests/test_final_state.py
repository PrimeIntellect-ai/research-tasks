# test_final_state.py

import os
import pytest

def test_executable_exists():
    """Test that the compiled C program exists and is executable."""
    executable_path = "/home/user/cleaner"
    assert os.path.exists(executable_path), f"Executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_normalized_csv_files_exist():
    """Test that the output CSV files exist."""
    assert os.path.exists("/home/user/train_norm.csv"), "/home/user/train_norm.csv is missing."
    assert os.path.exists("/home/user/test_norm.csv"), "/home/user/test_norm.csv is missing."

def test_test_norm_csv_contents():
    """Test that test_norm.csv has the correct normalized values (no data leakage)."""
    expected_content = "8,1.9640\n9,2.4004"
    with open("/home/user/test_norm.csv", "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Contents of test_norm.csv are incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_train_norm_csv_contents():
    """Test that train_norm.csv has the correct normalized values."""
    expected_lines = [
        "0,-1.5275",
        "1,-1.0911",
        "2,-0.6547",
        "3,-0.2182",
        "4,0.2182",
        "5,0.6547",
        "6,1.0911",
        "7,1.5275"
    ]
    with open("/home/user/train_norm.csv", "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 8, f"Expected 8 lines in train_norm.csv, got {len(lines)}."
    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} in train_norm.csv is incorrect. Expected {expected}, got {lines[i]}."

def test_benchmark_script_exists():
    """Test that the benchmark script exists."""
    assert os.path.exists("/home/user/benchmark.sh"), "/home/user/benchmark.sh is missing."

def test_benchmark_avg_exists_and_valid():
    """Test that benchmark_avg.txt exists and contains a valid float."""
    avg_file = "/home/user/benchmark_avg.txt"
    assert os.path.exists(avg_file), f"{avg_file} is missing."

    with open(avg_file, "r") as f:
        content = f.read().strip()

    assert content != "", f"{avg_file} is empty."

    try:
        avg_val = float(content)
    except ValueError:
        pytest.fail(f"Contents of {avg_file} ('{content}') cannot be parsed as a float.")

    assert avg_val >= 0.0, "Average execution time should be non-negative."