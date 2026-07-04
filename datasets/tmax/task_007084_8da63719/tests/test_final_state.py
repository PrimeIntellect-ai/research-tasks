# test_final_state.py

import os
import json
import math

def test_results_json_exists():
    """Check that the results.json file exists."""
    file_path = "/home/user/results.json"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

def test_results_json_values():
    """Compute the expected values from the CSV and verify the JSON output."""
    csv_path = "/home/user/sensor_data.csv"
    json_path = "/home/user/results.json"

    assert os.path.isfile(csv_path), f"The file {csv_path} is missing."
    assert os.path.isfile(json_path), f"The file {json_path} is missing."

    with open(csv_path, "r") as f:
        lines = f.read().strip().split('\n')

    header = lines[0].split(',')

    # Parse rows
    valid_rows = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split(',')
        sensor_1 = float(parts[1])
        # Outlier Handling
        if sensor_1 > 50.0:
            continue

        sensor_2_str = parts[2].strip()
        sensor_2 = float(sensor_2_str) if sensor_2_str else None
        sensor_3 = int(parts[3])
        outcome = int(parts[4])

        valid_rows.append({
            'sensor_1': sensor_1,
            'sensor_2': sensor_2,
            'sensor_3': sensor_3,
            'outcome': outcome
        })

    # Missing Value Imputation
    valid_sensor_2 = [r['sensor_2'] for r in valid_rows if r['sensor_2'] is not None]
    mean_sensor_2 = sum(valid_sensor_2) / len(valid_sensor_2) if valid_sensor_2 else 0.0

    # Impute
    for r in valid_rows:
        if r['sensor_2'] is None:
            r['sensor_2'] = mean_sensor_2

    # Covariance Analysis
    n = len(valid_rows)
    mean_sensor_1 = sum(r['sensor_1'] for r in valid_rows) / n

    covariance = sum((r['sensor_1'] - mean_sensor_1) * (r['sensor_2'] - mean_sensor_2) for r in valid_rows) / n

    # Bayesian Inference
    s3_1_rows = [r for r in valid_rows if r['sensor_3'] == 1]
    outcome_1_given_s3_1 = [r for r in s3_1_rows if r['outcome'] == 1]
    prob = len(outcome_1_given_s3_1) / len(s3_1_rows) if s3_1_rows else 0.0

    # Read JSON
    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not a valid JSON file."

    assert "imputed_mean_sensor_2" in data, "Missing 'imputed_mean_sensor_2' in JSON."
    assert "covariance_1_2" in data, "Missing 'covariance_1_2' in JSON."
    assert "prob_outcome_given_sensor_3" in data, "Missing 'prob_outcome_given_sensor_3' in JSON."

    assert math.isclose(data["imputed_mean_sensor_2"], mean_sensor_2, rel_tol=1e-3), \
        f"Expected imputed_mean_sensor_2 to be close to {mean_sensor_2}, got {data['imputed_mean_sensor_2']}"

    assert math.isclose(data["covariance_1_2"], covariance, rel_tol=1e-3), \
        f"Expected covariance_1_2 to be close to {covariance}, got {data['covariance_1_2']}"

    assert math.isclose(data["prob_outcome_given_sensor_3"], prob, rel_tol=1e-3), \
        f"Expected prob_outcome_given_sensor_3 to be close to {prob}, got {data['prob_outcome_given_sensor_3']}"