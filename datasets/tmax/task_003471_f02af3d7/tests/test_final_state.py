# test_final_state.py

import os
import sys

def test_cleaned_data_csv_exists():
    csv_path = '/home/user/cleaned_data.csv'
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"Expected {csv_path} to be a file."

def test_cleaned_data_header():
    csv_path = '/home/user/cleaned_data.csv'
    with open(csv_path, 'r') as f:
        header = f.readline().strip()
    expected_header = "ID,Value,Status"
    assert header == expected_header, f"Incorrect CSV header. Expected '{expected_header}', got '{header}'."

def test_f1_score_metric():
    csv_path = '/home/user/cleaned_data.csv'
    truth_path = '/app/valid_ids.txt'

    assert os.path.exists(truth_path), "Ground truth file missing."

    with open(truth_path, 'r') as f:
        ground_truth = set(line.strip() for line in f if line.strip())

    predicted = set()
    with open(csv_path, 'r') as f:
        header = f.readline().strip()
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 1 and parts[0]:
                predicted.add(parts[0])

    tp = len(predicted & ground_truth)
    fp = len(predicted - ground_truth)
    fn = len(ground_truth - predicted)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    threshold = 0.99
    assert f1 >= threshold, f"F1 Score is {f1:.4f}, which is below the threshold of {threshold}. TP={tp}, FP={fp}, FN={fn}."