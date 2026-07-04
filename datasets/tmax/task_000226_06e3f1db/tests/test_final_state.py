# test_final_state.py

import os
import json
import pandas as pd
import pytest

def test_anomaly_detection_f1_score():
    csv_path = '/home/user/data/readings.csv'
    json_path = '/home/user/anomalies.json'

    assert os.path.exists(csv_path), f"Missing CSV file: {csv_path}"
    assert os.path.exists(json_path), f"Missing JSON output file: {json_path}"

    # Load ground truth
    df = pd.read_csv(csv_path)
    anomalies = []
    for idx, row in df.iterrows():
        if row['sensor_name'] == 'Pressure_Sensor':
            if abs(row['value'] - 105.0) > 2.5 * 4.2:
                anomalies.append(int(row['row_id']))
        elif row['sensor_name'] == 'Temp_Sensor':
            if abs(row['value'] - 298.5) > 2.5 * 1.1:
                anomalies.append(int(row['row_id']))

    gt_set = set(anomalies)

    # Load agent output
    try:
        with open(json_path, 'r') as f:
            pred_list = json.load(f)
        pred_set = set(pred_list)
    except Exception as e:
        pytest.fail(f"Failed to read or parse {json_path}: {e}")

    # Calculate F1
    tp = len(gt_set.intersection(pred_set))
    fp = len(pred_set - gt_set)
    fn = len(gt_set - pred_set)

    if tp == 0:
        f1 = 0.0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 Score {f1:.4f} is below threshold 0.95. TP: {tp}, FP: {fp}, FN: {fn}"