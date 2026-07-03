# test_final_state.py

import os
import subprocess
import pytest

def test_best_threshold():
    path = "/home/user/best_threshold.txt"
    assert os.path.exists(path), f"File {path} is missing. Did you write the best threshold to this file?"
    with open(path, "r") as f:
        val = f.read().strip()
    assert val == "2.5", f"Expected best threshold to be 2.5, but got '{val}' in {path}."

def test_cleaned_dataset():
    path = "/home/user/cleaned_dataset.csv"
    assert os.path.exists(path), f"File {path} is missing. Did you save the cleaned dataset?"
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = {'E01', 'E02', 'E03', 'E05', 'E07', 'E08', 'E10', 'E11', 'E13'}
    actual_ids = set(lines)

    missing = expected_ids - actual_ids
    extra = actual_ids - expected_ids

    error_msg = f"Cleaned dataset IDs in {path} do not match the expected output."
    if missing:
        error_msg += f" Missing expected IDs: {missing}."
    if extra:
        error_msg += f" Found unexpected IDs: {extra}."

    assert actual_ids == expected_ids, error_msg

def test_filter_outliers_script_fixed():
    path = "/home/user/filter_outliers.sh"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    # Run the script with threshold 2.5 to verify it correctly parses floats now
    result = subprocess.run([path, "2.5"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute properly. Stderr: {result.stderr}"

    output_ids = set(result.stdout.strip().split('\n'))
    output_ids = {x for x in output_ids if x}  # Remove any empty strings

    expected_ids = {'E01', 'E02', 'E03', 'E05', 'E07', 'E08', 'E10', 'E11', 'E13'}

    missing = expected_ids - output_ids
    extra = output_ids - expected_ids

    error_msg = "The script filter_outliers.sh did not output the correct IDs for threshold 2.5. Is the locale/decimal bug fully fixed?"
    if missing:
        error_msg += f" Missing IDs: {missing}."
    if extra:
        error_msg += f" Unexpected IDs: {extra}."

    assert output_ids == expected_ids, error_msg