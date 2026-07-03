# test_final_state.py

import os
import csv
from collections import defaultdict

def test_results_csv_exists():
    assert os.path.exists("/home/user/results.csv"), "/home/user/results.csv does not exist. The C program may not have run or failed to create the output file."
    assert os.path.isfile("/home/user/results.csv"), "/home/user/results.csv is not a file."

def test_results_csv_content():
    experiments_file = "/home/user/experiments.csv"
    results_file = "/home/user/results.csv"

    assert os.path.exists(experiments_file), f"{experiments_file} is missing."

    # Recompute expected results dynamically
    stats = defaultdict(lambda: {'successes': 0, 'failures': 0, 'prior_alpha': 0, 'prior_beta': 0})

    with open(experiments_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 10:
                continue
            exp_id = row[0]
            f1, f2, f3 = float(row[1]), float(row[2]), float(row[3])
            w1, w2, w3 = float(row[4]), float(row[5]), float(row[6])
            target = float(row[7])
            prior_alpha = int(row[8])
            prior_beta = int(row[9])

            stats[exp_id]['prior_alpha'] = prior_alpha
            stats[exp_id]['prior_beta'] = prior_beta

            prediction = (f1 * w1) + (f2 * w2) + (f3 * w3)
            if abs(prediction - target) < 0.1:
                stats[exp_id]['successes'] += 1
            else:
                stats[exp_id]['failures'] += 1

    expected_lines = []
    for exp_id in sorted(stats.keys()):
        post_alpha = stats[exp_id]['prior_alpha'] + stats[exp_id]['successes']
        post_beta = stats[exp_id]['prior_beta'] + stats[exp_id]['failures']
        ev = post_alpha / (post_alpha + post_beta)
        expected_lines.append(f"{exp_id},{post_alpha},{post_beta},{ev:.4f}")

    with open(results_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in results.csv, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Row {i+1} mismatch. Expected '{expected}', but got '{actual}'."