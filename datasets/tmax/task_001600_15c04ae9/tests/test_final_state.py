# test_final_state.py

import os
import re

def test_c_file_exists():
    path = "/home/user/embed_prep.c"
    assert os.path.isfile(path), f"Missing C source file: {path}"

def test_nearest_neighbors_csv():
    actual_path = "/home/user/nearest_neighbors.csv"
    expected_path = "/home/user/expected_neighbors.csv"

    assert os.path.isfile(actual_path), f"Missing output file: {actual_path}"
    assert os.path.isfile(expected_path), f"Missing expected file: {expected_path}"

    with open(actual_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    with open(expected_path, "r") as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Line count mismatch: expected {len(expected_lines)}, got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1}: expected '{expected}', got '{actual}'"

def test_benchmark_txt():
    path = "/home/user/benchmark.txt"
    assert os.path.isfile(path), f"Missing benchmark file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    pattern = r"^Search time: \d+\.\d+ seconds$"
    assert re.match(pattern, content), f"Benchmark file content '{content}' does not match expected format '{pattern}'"