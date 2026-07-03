# test_final_state.py

import os
import json
import csv
import math
import pytest

def get_sensor_data():
    data_path = "/home/user/data/sensor_data.csv"
    assert os.path.isfile(data_path), f"File missing: {data_path}"
    f1, f2 = [], []
    with open(data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            f1.append(float(row['feature1']))
            f2.append(float(row['feature2']))
    return f1, f2

def calculate_pearson(x, y):
    n = len(x)
    if n == 0: return 0.0
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = sum((xi - mean_x)**2 for xi in x)
    den_y = sum((yi - mean_y)**2 for yi in y)
    if den_x == 0 or den_y == 0: return 0.0
    return num / math.sqrt(den_x * den_y)

def calculate_expanding_zscore_predictions(f1):
    preds = []
    for i in range(len(f1)):
        if i == 0 or i == 1:
            z = 0.0
        else:
            window = f1[:i]
            mean = sum(window) / len(window)
            variance = sum((x - mean)**2 for x in window) / (len(window) - 1)
            std_dev = math.sqrt(variance)
            if std_dev == 0.0:
                z = 0.0
            else:
                z = (f1[i] - mean) / std_dev
        pred = z * 0.5 + 1.2
        preds.append(pred)
    return preds

def test_experiment_log():
    log_path = "/home/user/experiment_log.json"
    assert os.path.isfile(log_path), f"Experiment log missing: {log_path}"

    with open(log_path, 'r') as f:
        try:
            log_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Experiment log {log_path} is not valid JSON.")

    assert "experiment_name" in log_data, "Missing 'experiment_name' in experiment log."
    assert log_data["experiment_name"] == "fix_data_leakage", "Incorrect 'experiment_name'."

    assert "pearson_correlation_feature1_feature2" in log_data, "Missing 'pearson_correlation_feature1_feature2' in experiment log."

    f1, f2 = get_sensor_data()
    expected_corr = calculate_pearson(f1, f2)
    expected_corr_rounded = round(expected_corr, 4)

    actual_corr = log_data["pearson_correlation_feature1_feature2"]
    assert isinstance(actual_corr, float), "Pearson correlation value should be a float."
    assert math.isclose(actual_corr, expected_corr_rounded, abs_tol=1e-4), \
        f"Expected Pearson correlation ~{expected_corr_rounded}, but got {actual_corr}"

def test_predictions_csv():
    preds_path = "/home/user/pipeline/build/predictions.csv"
    assert os.path.isfile(preds_path), f"Predictions CSV missing: {preds_path}. Did you build and run the pipeline?"

    f1, _ = get_sensor_data()
    expected_preds = calculate_expanding_zscore_predictions(f1)

    actual_preds = []
    with open(preds_path, 'r') as f:
        reader = csv.DictReader(f)
        assert "id" in reader.fieldnames and "pred" in reader.fieldnames, "predictions.csv header is incorrect."
        for row in reader:
            actual_preds.append(float(row['pred']))

    assert len(actual_preds) == len(expected_preds), f"Expected {len(expected_preds)} predictions, found {len(actual_preds)}"

    for i, (actual, expected) in enumerate(zip(actual_preds, expected_preds)):
        expected_rounded = round(expected, 4)
        assert math.isclose(actual, expected_rounded, abs_tol=1e-3), \
            f"Prediction mismatch at index {i}: Expected ~{expected_rounded}, got {actual}. Check expanding window logic."