# test_final_state.py
import os
import csv
import math

def test_files_exist():
    required_files = [
        "/home/user/compute_variance.c",
        "/home/user/evaluate.sh",
        "/home/user/fold_variances.csv"
    ]
    for path in required_files:
        assert os.path.isfile(path), f"Required file {path} is missing."

def test_csv_results():
    expected_path = "/home/user/expected_variances.csv"
    actual_path = "/home/user/fold_variances.csv"

    assert os.path.isfile(expected_path), f"Truth file {expected_path} is missing."
    assert os.path.isfile(actual_path), f"Output file {actual_path} is missing."

    with open(expected_path, 'r') as f:
        expected_reader = csv.DictReader(f)
        expected_data = {row['Fold'].strip(): float(row['Trace'].strip()) for row in expected_reader}

    with open(actual_path, 'r') as f:
        actual_reader = csv.DictReader(f)
        assert 'Fold' in actual_reader.fieldnames and 'Trace' in actual_reader.fieldnames, \
            "Output CSV must have 'Fold' and 'Trace' headers."
        actual_data = {row['Fold'].strip(): float(row['Trace'].strip()) for row in actual_reader}

    for fold in [str(i) for i in range(5)]:
        assert fold in actual_data, f"Fold {fold} missing in output CSV."
        expected_val = expected_data[fold]
        actual_val = actual_data[fold]
        assert math.isclose(expected_val, actual_val, rel_tol=1e-3, abs_tol=1e-3), \
            f"Trace value mismatch for fold {fold}: expected approx {expected_val:.4f}, got {actual_val:.4f}."