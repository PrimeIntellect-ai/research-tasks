# test_final_state.py

import os
import math
import pytest

def test_processed_data_csv_fixed():
    path = "/home/user/processed_data.csv"
    assert os.path.isfile(path), f"Missing file: {path}. Did you run the pipeline?"
    with open(path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 1, f"File {path} is empty or missing data."

    # Check that IDs are integers and no empty IDs exist
    for line in lines[1:]:
        parts = line.split(',')
        assert len(parts) >= 2, f"Invalid format in {path}: {line}"
        id_val = parts[0].strip()
        assert id_val != "", f"Found missing ID in {path}. Rows with missing IDs should be dropped."
        assert '.' not in id_val, f"ID is not an integer in {path}: '{id_val}'. It must be cast to int."

def test_joined_csv_not_empty():
    path = "/home/user/joined.csv"
    assert os.path.isfile(path), f"Missing file: {path}. Did you run the pipeline?"
    with open(path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 6, f"Expected 6 joined rows in {path}, got {len(lines)}. The join command failed to match correctly."

def test_results_txt_valid():
    path = "/home/user/results.txt"
    assert os.path.isfile(path), f"Missing file: {path}. Did you run the pipeline?"
    with open(path, "r") as f:
        content = f.read()

    assert "p-value: NaN" not in content, "results.txt contains 'p-value: NaN'. The T-test failed due to empty or invalid data."
    assert "p-value:" in content, "results.txt does not contain the expected 'p-value:' output."

def test_final_p_value_txt_correct():
    path = "/home/user/final_p_value.txt"
    assert os.path.isfile(path), f"Missing file: {path}. You must create this file with the extracted p-value."
    with open(path, "r") as f:
        content = f.read().strip()

    try:
        p_val = float(content)
    except ValueError:
        pytest.fail(f"final_p_value.txt does not contain a valid numeric float: '{content}'")

    # Calculate expected p-value based on text lengths
    # Group A: len("hello world")=11, len("testing embeddings here")=23, len("short")=5
    # Group B: len("another text")=12, len("foo bar baz")=11, len("a bit longer text for group B")=29
    expected_p = 0.7410940562489656

    assert math.isclose(p_val, expected_p, rel_tol=1e-3), f"Extracted p-value {p_val} is incorrect. Expected approximately {expected_p}."