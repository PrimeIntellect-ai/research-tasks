# test_final_state.py

import os
import csv
import pytest

def test_bayes_results_correctness():
    dataset_path = "/home/user/dataset.csv"
    results_path = "/home/user/bayes_results.txt"

    assert os.path.exists(dataset_path), f"Dataset file missing at {dataset_path}"
    assert os.path.exists(results_path), f"Results file missing at {results_path}"

    # Derive expected values from the dataset
    valid_rows = []
    with open(dataset_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                feature_x = float(row['feature_x'])
                target = int(row['target'])
            except ValueError:
                continue

            if feature_x == -999:
                continue

            feat_bin = 1 if feature_x > 50 else 0
            valid_rows.append({'feat_bin': feat_bin, 'target': target})

    total_valid = len(valid_rows)
    assert total_valid > 0, "No valid rows found in dataset."

    target_1_count = sum(1 for r in valid_rows if r['target'] == 1)
    target_0_count = sum(1 for r in valid_rows if r['target'] == 0)

    prior_t1 = target_1_count / total_valid

    if target_1_count > 0:
        likelihood_f1_t1 = sum(1 for r in valid_rows if r['target'] == 1 and r['feat_bin'] == 1) / target_1_count
    else:
        likelihood_f1_t1 = 0.0

    if target_0_count > 0:
        likelihood_f1_t0 = sum(1 for r in valid_rows if r['target'] == 0 and r['feat_bin'] == 1) / target_0_count
    else:
        likelihood_f1_t0 = 0.0

    expected_prior_t1_str = f"{prior_t1:.4f}"
    expected_likelihood_f1_t1_str = f"{likelihood_f1_t1:.4f}"
    expected_likelihood_f1_t0_str = f"{likelihood_f1_t0:.4f}"

    expected_lines = [
        f"Prior_T1: {expected_prior_t1_str}",
        f"Likelihood_F1_given_T1: {expected_likelihood_f1_t1_str}",
        f"Likelihood_F1_given_T0: {expected_likelihood_f1_t0_str}"
    ]

    with open(results_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 3, f"Expected 3 lines in {results_path}, found {len(actual_lines)}"

    assert actual_lines[0] == expected_lines[0], f"Line 1 mismatch. Expected '{expected_lines[0]}', got '{actual_lines[0]}'"
    assert actual_lines[1] == expected_lines[1], f"Line 2 mismatch. Expected '{expected_lines[1]}', got '{actual_lines[1]}'"
    assert actual_lines[2] == expected_lines[2], f"Line 3 mismatch. Expected '{expected_lines[2]}', got '{actual_lines[2]}'"