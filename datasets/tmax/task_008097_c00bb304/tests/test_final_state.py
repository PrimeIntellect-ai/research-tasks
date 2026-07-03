# test_final_state.py

import os
import pytest

def test_executable_exists():
    """Test that the C program was compiled."""
    assert os.path.isfile("/home/user/src/normalize"), "Compiled executable /home/user/src/normalize does not exist."
    assert os.access("/home/user/src/normalize", os.X_OK), "/home/user/src/normalize is not executable."

def test_c_code_fixed():
    """Test that the C code was modified to fix the data leak."""
    filepath = "/home/user/src/normalize.c"
    assert os.path.isfile(filepath), f"{filepath} missing."

    with open(filepath, "r") as f:
        content = f.read()

    # The original loop was `for (int i = 0; i < NUM_ROWS; i++)` for min/max.
    # We can't strictly assert the exact syntax they used, but we can verify 
    # the output files to ensure correctness.

def test_train_scaled_csv():
    """Test that train_scaled.csv was generated and scaled correctly."""
    filepath = "/home/user/out/train_scaled.csv"
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 8, f"Expected 8 rows in train_scaled.csv, found {len(lines)}."

    # Check first and last row of train to ensure correct scaling.
    # Min for both features in train is 1.0, Max is 8.0. Range is 7.0.
    # First row: 1.0, 2.0 -> (1-1)/7 = 0.0, (2-1)/7 = 1/7 = 0.142857
    parts_first = lines[0].split(',')
    assert abs(float(parts_first[0]) - 0.0) < 1e-4, "First feature of first train row is incorrect."
    assert abs(float(parts_first[1]) - 0.142857) < 1e-4, "Second feature of first train row is incorrect."
    assert int(parts_first[2]) == 0, "Label of first train row is incorrect."

def test_test_scaled_csv():
    """Test that test_scaled.csv was generated using ONLY train min/max."""
    filepath = "/home/user/out/test_scaled.csv"
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected 2 rows in test_scaled.csv, found {len(lines)}."

    # Row 9 (original): 9.0, 10.0, 0
    # Scaled: (9-1)/7 = 8/7 = 1.142857, (10-1)/7 = 9/7 = 1.285714
    parts_0 = lines[0].split(',')
    assert abs(float(parts_0[0]) - 1.142857) < 1e-4, "Data leak not fixed: test feature 0 scaled incorrectly."
    assert abs(float(parts_0[1]) - 1.285714) < 1e-4, "Data leak not fixed: test feature 1 scaled incorrectly."
    assert int(parts_0[2]) == 0, "Label of first test row is incorrect."

    # Row 10 (original): 10.0, 9.0, 1
    # Scaled: (10-1)/7 = 9/7 = 1.285714, (9-1)/7 = 8/7 = 1.142857
    parts_1 = lines[1].split(',')
    assert abs(float(parts_1[0]) - 1.285714) < 1e-4, "Data leak not fixed: test feature 0 scaled incorrectly."
    assert abs(float(parts_1[1]) - 1.142857) < 1e-4, "Data leak not fixed: test feature 1 scaled incorrectly."
    assert int(parts_1[2]) == 1, "Label of second test row is incorrect."

def test_covariance_txt():
    """Test that the covariance text file contains the correct value."""
    filepath = "/home/user/out/test_covariance.txt"
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content == "-0.0102", f"Expected covariance to be '-0.0102', but found '{content}'."