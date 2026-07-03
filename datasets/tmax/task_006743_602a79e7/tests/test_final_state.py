# test_final_state.py

import os
import csv
import math
import re

def get_expected_ci():
    def read_csv(filepath):
        data = []
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    train = read_csv('/home/user/train_metrics.csv')
    test = read_csv('/home/user/test_metrics.csv')
    meta = read_csv('/home/user/metadata.csv')

    meta_ids = {row['experiment_id'] for row in meta}

    train_losses = [float(row['loss_score']) for row in train if row['experiment_id'] in meta_ids]
    test_losses = [float(row['loss_score']) for row in test if row['experiment_id'] in meta_ids]

    assert len(train_losses) > 0, "No valid training data found after join."
    assert len(test_losses) > 0, "No valid test data found after join."

    train_mean = sum(train_losses) / len(train_losses)
    train_sq_sum = sum((x - train_mean)**2 for x in train_losses)
    train_std = math.sqrt(train_sq_sum / len(train_losses))

    test_norm = [(x - train_mean) / train_std for x in test_losses]

    test_norm_mean = sum(test_norm) / len(test_norm)
    test_norm_sq_sum = sum((x - test_norm_mean)**2 for x in test_norm)
    test_norm_std = math.sqrt(test_norm_sq_sum / len(test_norm))

    margin = 1.96 * (test_norm_std / math.sqrt(len(test_norm)))

    return test_norm_mean - margin, test_norm_mean + margin

def test_ci_output_exists_and_correct():
    ci_file = '/home/user/test_ci.txt'
    assert os.path.exists(ci_file), f"The output file {ci_file} does not exist. Did you run the C++ pipeline and output to the correct path?"

    with open(ci_file, 'r') as f:
        content = f.read().strip()

    match = re.match(r'^\[\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*\]$', content)
    assert match, f"Output format in {ci_file} is incorrect. Expected format '[lower_bound, upper_bound]', got: '{content}'"

    actual_lower, actual_upper = float(match.group(1)), float(match.group(2))
    expected_lower, expected_upper = get_expected_ci()

    assert math.isclose(actual_lower, expected_lower, abs_tol=1e-3), \
        f"Lower bound {actual_lower} does not match expected {expected_lower:.4f}. Check your normalization and CI logic."
    assert math.isclose(actual_upper, expected_upper, abs_tol=1e-3), \
        f"Upper bound {actual_upper} does not match expected {expected_upper:.4f}. Check your normalization and CI logic."

def test_pipeline_binary_exists():
    binary_path = '/home/user/etl_pipeline'
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist. Did you compile the code as instructed?"
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."