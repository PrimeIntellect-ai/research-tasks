# test_final_state.py

import os
import pytest
import numpy as np

def test_outliers_txt_correct():
    outliers_file = '/home/user/outliers.txt'
    true_outliers_file = '/home/user/.true_outliers.npy'

    assert os.path.exists(outliers_file), f"File {outliers_file} is missing."
    assert os.path.exists(true_outliers_file), f"Truth file {true_outliers_file} is missing."

    # Load true outliers
    try:
        true_outliers = np.load(true_outliers_file)
    except Exception as e:
        pytest.fail(f"Failed to load {true_outliers_file}: {e}")

    # Read student's outliers
    with open(outliers_file, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 50, f"Expected exactly 50 outliers in {outliers_file}, found {len(lines)}"

    try:
        student_outliers = [int(line.strip()) for line in lines if line.strip()]
    except ValueError:
        pytest.fail(f"All lines in {outliers_file} must be integers.")

    assert len(student_outliers) == 50, f"Expected 50 valid integer lines, got {len(student_outliers)}"

    # Check if sorted
    assert student_outliers == sorted(student_outliers), f"Indices in {outliers_file} are not sorted in ascending order."

    # Compare with truth
    student_outliers_arr = np.array(student_outliers)
    if not np.array_equal(student_outliers_arr, true_outliers):
        pytest.fail(f"Indices in {outliers_file} do not exactly match the expected true outliers.")

def test_clean_embeddings_correct():
    clean_file = '/home/user/clean_embeddings.npy'

    assert os.path.exists(clean_file), f"File {clean_file} is missing."

    try:
        clean_data = np.load(clean_file)
    except Exception as e:
        pytest.fail(f"Failed to load {clean_file}: {e}")

    expected_shape = (950, 10)
    assert clean_data.shape == expected_shape, f"Expected clean_embeddings.npy to have shape {expected_shape}, got {clean_data.shape}"