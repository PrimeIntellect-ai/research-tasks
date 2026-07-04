# test_final_state.py

import os
import json
import csv
import math
import statistics
import pytest

def get_pearson_corr(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = sum((xi - mean_x) ** 2 for xi in x)
    den_y = sum((yi - mean_y) ** 2 for yi in y)
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / math.sqrt(den_x * den_y)

def test_pipeline_results_json():
    json_path = "/home/user/pipeline_results.json"
    csv_path = "/home/user/data/sensor_log.csv"

    assert os.path.exists(json_path), f"The result file is missing: {json_path}"

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert "dropped_columns" in results, "Missing 'dropped_columns' in JSON."
    assert "best_params" in results, "Missing 'best_params' in JSON."
    assert "mse" in results, "Missing 'mse' in JSON."

    # Compute expected dropped columns using stdlib
    assert os.path.exists(csv_path), f"The dataset file is missing: {csv_path}"

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        data = {field: [] for field in reader.fieldnames}
        for row in reader:
            for field in reader.fieldnames:
                data[field].append(row[field])

    # Impute event_count
    event_counts = [float(v) for v in data['event_count'] if v.strip() != '']
    median_ec = statistics.median(event_counts)

    imputed_ec = []
    for v in data['event_count']:
        if v.strip() == '':
            imputed_ec.append(int(median_ec))
        else:
            imputed_ec.append(int(float(v)))

    data['event_count'] = imputed_ec

    for field in ['sensor_1', 'sensor_2', 'sensor_3']:
        data[field] = [float(v) for v in data[field]]

    features = [f for f in data.keys() if f != 'system_load']
    expected_dropped = []

    s1 = data['sensor_1']
    for f in features:
        if f == 'sensor_1':
            continue
        corr = abs(get_pearson_corr(s1, data[f]))
        if corr > 0.80:
            expected_dropped.append(f)

    expected_dropped.sort()

    assert results["dropped_columns"] == expected_dropped, \
        f"Expected dropped_columns to be {expected_dropped}, but got {results['dropped_columns']}."

    # Check best_params structure
    expected_params = {"alpha_1", "alpha_2", "lambda_1", "lambda_2"}
    assert set(results["best_params"].keys()) == expected_params, \
        f"Expected best_params keys to be {expected_params}, but got {set(results['best_params'].keys())}."

    valid_values = {1e-6, 1e-2}
    for k, v in results["best_params"].items():
        assert v in valid_values, f"Parameter {k} has invalid value {v}. Must be one of {valid_values}."

    # Check mse
    assert isinstance(results["mse"], (int, float)), "MSE must be a number."
    assert results["mse"] > 0, "MSE should be positive."

    # Check rounding to 4 decimal places
    mse_str = str(results["mse"])
    if "." in mse_str:
        decimals = len(mse_str.split(".")[1])
        assert decimals <= 4, f"MSE {results['mse']} is not rounded to 4 decimal places."