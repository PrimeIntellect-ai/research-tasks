# test_final_state.py

import os
import pytest

def calculate_f1(pred_file, truth_file):
    try:
        with open(pred_file, 'r') as f:
            preds = set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return 0.0

    with open(truth_file, 'r') as f:
        truths = set(line.strip() for line in f if line.strip())

    if not preds and not truths:
        return 1.0
    if not preds or not truths:
        return 0.0

    tp = len(preds.intersection(truths))
    fp = len(preds - truths)
    fn = len(truths - preds)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    if precision + recall == 0:
        return 0.0

    f1 = 2 * (precision * recall) / (precision + recall)
    return f1

def test_valid_artifacts_f1_score():
    pred_file = '/home/user/valid_artifacts.txt'
    truth_file = '/app/ground_truth_valid.txt'

    assert os.path.exists(truth_file), f"Ground truth file {truth_file} is missing."
    assert os.path.exists(pred_file), f"Student output file {pred_file} is missing."

    f1_score = calculate_f1(pred_file, truth_file)

    threshold = 0.95
    assert f1_score >= threshold, f"F1 Score of {f1_score:.4f} is below the required threshold of {threshold}."