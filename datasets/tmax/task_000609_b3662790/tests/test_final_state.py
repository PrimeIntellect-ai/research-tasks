# test_final_state.py

import os
import csv
import math
import pytest

def get_expected_test_mean():
    data_path = "/home/user/data.csv"
    if not os.path.exists(data_path):
        return None

    train_vals = []
    test_vals = []

    with open(data_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = float(row['value'])
            if row['split'] == 'train':
                train_vals.append(val)
            elif row['split'] == 'test':
                test_vals.append(val)

    if not train_vals or not test_vals:
        return None

    train_mean = sum(train_vals) / len(train_vals)
    sq_sum = sum((x - train_mean)**2 for x in train_vals)
    train_std = math.sqrt(sq_sum / len(train_vals))

    test_norms = [(x - train_mean) / train_std for x in test_vals]
    test_mean = sum(test_norms) / len(test_norms)

    return test_mean

def test_test_mean_output():
    out_path = "/home/user/test_mean.txt"
    assert os.path.exists(out_path), f"Output file {out_path} is missing. Did you compile and run the C program?"

    with open(out_path, "r") as f:
        content = f.read().strip()

    assert content, f"{out_path} is empty."

    try:
        actual_test_mean = float(content)
    except ValueError:
        pytest.fail(f"Could not parse a float from {out_path}. Content: {content}")

    expected_test_mean = get_expected_test_mean()
    assert expected_test_mean is not None, "Could not compute expected test mean due to missing or invalid data.csv."

    # Original leaky test_mean was ~0.5898. Expected is ~0.9038.
    assert math.isclose(actual_test_mean, expected_test_mean, abs_tol=0.001), \
        f"test_mean.txt contains {actual_test_mean:.4f}, but expected {expected_test_mean:.4f}. The data leakage bug might not be correctly fixed."

def test_bootstrap_mean_output():
    out_path = "/home/user/bootstrap_mean.txt"
    assert os.path.exists(out_path), f"Output file {out_path} is missing."

    with open(out_path, "r") as f:
        content = f.read().strip()

    assert content, f"{out_path} is empty."

    try:
        actual_bs_mean = float(content)
    except ValueError:
        pytest.fail(f"Could not parse a float from {out_path}. Content: {content}")

    # Original leaky bootstrap_mean was ~-0.1652.
    # Fixed bootstrap_mean samples from train data normalized by its own mean, 
    # so the expected value should be very close to 0.0 (e.g., ~0.0039).
    assert abs(actual_bs_mean) < 0.05, \
        f"bootstrap_mean.txt contains {actual_bs_mean:.4f}, which is too far from 0.0. " \
        "If normalization was correctly computed ONLY on the train split, the train split's normalized mean should be 0."

def test_c_code_modifications():
    c_path = "/home/user/normalize_and_bootstrap.c"
    assert os.path.exists(c_path), f"C program {c_path} is missing."

    with open(c_path, "r") as f:
        code = f.read()

    # Basic heuristic checks to ensure the student didn't just hardcode the outputs
    assert "fopen(\"/home/user/test_mean.txt\"" in code, "Output file path for test_mean.txt was altered or removed."
    assert "fopen(\"/home/user/bootstrap_mean.txt\"" in code, "Output file path for bootstrap_mean.txt was altered or removed."
    assert "srand(42);" in code, "Random seed was altered or removed."
    assert "B = 1000;" in code or "b < 1000;" in code or "B=1000;" in code, "Number of bootstrap iterations was altered."