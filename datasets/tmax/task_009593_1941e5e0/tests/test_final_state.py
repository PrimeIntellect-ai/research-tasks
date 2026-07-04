# test_final_state.py

import os
import json
import csv
import math
import pytest

def get_valid_data():
    sensors_path = '/home/user/sensors.csv'
    labels_path = '/home/user/labels.csv'

    assert os.path.exists(sensors_path), f"Missing {sensors_path}"
    assert os.path.exists(labels_path), f"Missing {labels_path}"

    sensors = {}
    with open(sensors_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                s1 = float(row['sensor1'])
                s2 = float(row['sensor2'])
                s3 = float(row['sensor3'])
                sensors[row['id']] = (s1, s2, s3)
            except ValueError:
                continue

    labels = {}
    with open(labels_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lbl = row['label']
            if lbl in ('0', '1'):
                labels[row['id']] = int(lbl)

    joined_data = []
    for uid in sensors:
        if uid in labels:
            joined_data.append({
                'id': uid,
                's1': sensors[uid][0],
                's2': sensors[uid][1],
                's3': sensors[uid][2],
                'label': labels[uid]
            })

    return joined_data

def compute_expected_metrics(data):
    n = len(data)
    assert n > 1, "Not enough valid rows to compute covariance (N > 1 required)."

    label_1_count = sum(1 for d in data if d['label'] == 1)
    p_label_1 = label_1_count / n

    s1_gt_half_given_1 = sum(1 for d in data if d['label'] == 1 and d['s1'] > 0.5)
    p_s1_gt_half_given_label_1 = s1_gt_half_given_1 / label_1_count if label_1_count > 0 else 0.0

    label_0_count = sum(1 for d in data if d['label'] == 0)
    s1_gt_half_given_0 = sum(1 for d in data if d['label'] == 0 and d['s1'] > 0.5)
    p_s1_gt_half_given_label_0 = s1_gt_half_given_0 / label_0_count if label_0_count > 0 else 0.0

    means = [
        sum(d['s1'] for d in data) / n,
        sum(d['s2'] for d in data) / n,
        sum(d['s3'] for d in data) / n
    ]

    cov = [[0.0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            s_i = [d[f's{i+1}'] for d in data]
            s_j = [d[f's{j+1}'] for d in data]
            covar = sum((x - means[i]) * (y - means[j]) for x, y in zip(s_i, s_j)) / (n - 1)
            cov[i][j] = covar

    return {
        "valid_rows": n,
        "p_label_1": p_label_1,
        "p_s1_gt_half_given_label_1": p_s1_gt_half_given_label_1,
        "p_s1_gt_half_given_label_0": p_s1_gt_half_given_label_0,
        "covariance_matrix": cov
    }

def test_etl_results():
    json_path = '/home/user/etl_results.json'
    assert os.path.exists(json_path), f"Output file {json_path} does not exist. C program may not have run or failed."

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    expected = compute_expected_metrics(get_valid_data())

    assert "valid_rows" in results, "Missing 'valid_rows' in JSON output."
    assert results["valid_rows"] == expected["valid_rows"], f"Expected {expected['valid_rows']} valid rows, got {results['valid_rows']}."

    keys_to_check = [
        "p_label_1",
        "p_s1_gt_half_given_label_1",
        "p_s1_gt_half_given_label_0"
    ]

    for key in keys_to_check:
        assert key in results, f"Missing '{key}' in JSON output."
        assert isinstance(results[key], (int, float)), f"'{key}' must be a float."
        assert math.isclose(results[key], expected[key], abs_tol=1e-3), \
            f"Expected {key} to be ~{expected[key]:.4f}, got {results[key]}."

    assert "covariance_matrix" in results, "Missing 'covariance_matrix' in JSON output."
    cov_matrix = results["covariance_matrix"]
    assert len(cov_matrix) == 3 and all(len(row) == 3 for row in cov_matrix), \
        "Covariance matrix must be 3x3."

    for i in range(3):
        for j in range(3):
            val = cov_matrix[i][j]
            exp_val = expected["covariance_matrix"][i][j]
            assert isinstance(val, (int, float)), f"Covariance matrix at [{i}][{j}] must be a float."
            assert math.isclose(val, exp_val, abs_tol=1e-3), \
                f"Covariance matrix at [{i}][{j}] expected ~{exp_val:.4f}, got {val}."