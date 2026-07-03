# test_final_state.py

import os
import pytest

def calculate_f1(pred_file, truth_file):
    with open(pred_file, 'r') as f:
        preds = set(line.strip() for line in f if line.strip())
    with open(truth_file, 'r') as f:
        truth = set(line.strip() for line in f if line.strip())

    tp = len(preds & truth)
    fp = len(preds - truth)
    fn = len(truth - preds)

    if tp == 0:
        return 0.0

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1

def test_non_compliant_f1_score():
    pred_file = '/home/user/non_compliant.txt'
    truth_file = '/app/hidden_truth.txt'

    assert os.path.isfile(pred_file), f"Expected output file not found at {pred_file}"
    assert os.path.isfile(truth_file), f"Hidden truth file not found at {truth_file}"

    f1_score = calculate_f1(pred_file, truth_file)
    threshold = 0.95

    assert f1_score >= threshold, f"F1 Score {f1_score:.4f} is below the required threshold of {threshold}. Predictions did not match the ground truth closely enough."