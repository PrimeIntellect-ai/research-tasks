# test_final_state.py

import os
import pytest

def test_singular_values_file_exists():
    """Verify that the singular_values.txt file exists."""
    file_path = "/home/user/singular_values.txt"
    assert os.path.exists(file_path), f"Missing required file: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"

def test_singular_values_content():
    """Verify the contents of singular_values.txt match the expected singular values."""
    file_path = "/home/user/singular_values.txt"
    assert os.path.exists(file_path), f"Missing required file: {file_path}"

    expected_values = [
        "16.4827",
        "11.6033",
        "1.1416",
        "0.9996",
        "0.8711"
    ]

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_values), f"Expected {len(expected_values)} singular values, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_values)):
        assert actual == expected, f"Mismatch at line {i+1}: expected {expected}, got {actual}."

def test_pca_plot_exists_and_valid():
    """Verify that pca_plot.png exists and has a valid PNG signature."""
    file_path = "/home/user/pca_plot.png"
    assert os.path.exists(file_path), f"Missing required file: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"
    assert os.path.getsize(file_path) > 0, f"File is empty: {file_path}"

    # Check PNG magic number
    with open(file_path, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', f"File {file_path} is not a valid PNG image."