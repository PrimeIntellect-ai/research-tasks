# test_final_state.py

import os
import csv
import json

def test_anomalies_csv_exists_and_format():
    path = '/home/user/anomalies.csv'
    assert os.path.exists(path), f"Output file {path} is missing. The task requires writing anomalies to this path."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, f"The file {path} is empty. It must contain a header and the anomalous records."
        expected_header = ['timestamp', 'sensor', 'corrected_value']
        assert header == expected_header, f"Incorrect header in {path}. Expected {expected_header}, got {header}"

def test_f1_score_metric():
    path = '/home/user/anomalies.csv'
    assert os.path.exists(path), f"Cannot calculate metric: output file {path} is missing."

    gt_path = '/tmp/ground_truth_anomalies.json'
    assert os.path.exists(gt_path), f"Ground truth file {gt_path} is missing."

    with open(gt_path, 'r', encoding='utf-8') as f:
        gt_data = json.load(f)

    gt_timestamps = set(str(r['timestamp']) for r in gt_data)

    pred_timestamps = set()
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'timestamp' in row:
                pred_timestamps.add(row['timestamp'].strip())

    tp = len(gt_timestamps.intersection(pred_timestamps))
    fp = len(pred_timestamps - gt_timestamps)
    fn = len(gt_timestamps - pred_timestamps)

    if tp == 0:
        f1 = 0.0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.90, (
        f"Metric threshold failed: F1-Score is {f1:.4f}, which is below the required threshold of 0.90. "
        f"Stats: True Positives={tp}, False Positives={fp}, False Negatives={fn}."
    )