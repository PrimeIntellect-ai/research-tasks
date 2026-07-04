# test_final_state.py

import os
import csv
from collections import defaultdict

def test_report_csv_correctness():
    report_path = "/home/user/report.csv"
    assert os.path.isfile(report_path), f"Output file {report_path} is missing. Did you run your C++ program?"

    configs_path = "/home/user/configs.csv"
    metrics_path = "/home/user/metrics.csv"
    weights_path = "/home/user/weights.txt"

    assert os.path.isfile(configs_path), f"{configs_path} is missing."
    assert os.path.isfile(metrics_path), f"{metrics_path} is missing."
    assert os.path.isfile(weights_path), f"{weights_path} is missing."

    # Read weights
    with open(weights_path, "r") as f:
        weights = [float(line.strip()) for line in f if line.strip()]

    # Read configs
    run_to_model = {}
    with open(configs_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_to_model[row['run_id']] = row['model_type']

    # Read metrics and compute scores
    model_scores = defaultdict(list)
    with open(metrics_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_id = row['run_id']
            metrics = [
                float(row['m1']),
                float(row['m2']),
                float(row['m3']),
                float(row['m4']),
                float(row['m5'])
            ]
            score = sum(m * w for m, w in zip(metrics, weights))
            model_type = run_to_model[run_id]
            model_scores[model_type].append(score)

    # Compute means and sort
    model_means = []
    for model_type, scores in model_scores.items():
        mean_score = sum(scores) / len(scores)
        model_means.append((model_type, mean_score))

    model_means.sort(key=lambda x: x[1], reverse=True)

    # Format expected output
    expected_lines = [f"{model_type},{mean_score:.4f}" for model_type, mean_score in model_means]

    # Read actual output
    with open(report_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in report.csv, got {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'"