# test_final_state.py
import os
import csv
import json
import urllib.request
from urllib.error import URLError

def test_processed_csv_exists_and_correct():
    processed_path = '/home/user/processed_housing.csv'
    assert os.path.exists(processed_path), f"Processed CSV not found at {processed_path}"

    with open(processed_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        assert fieldnames is not None, "CSV file is empty or missing header"
        assert 'zip_code_encoded' in fieldnames, "Column 'zip_code_encoded' missing in processed CSV"

        found_99999 = False
        for row in reader:
            if row.get('zip_code') == '99999':
                found_99999 = True
                encoded_val = float(row['zip_code_encoded'])
                expected_val = 700312.5
                assert abs(encoded_val - expected_val) < 0.1, \
                    f"Incorrect smoothed value for 99999. Expected ~{expected_val}, got {encoded_val}"
                break

        assert found_99999, "Row with zip_code '99999' not found in processed CSV"

def test_mlflow_tracking():
    url = "http://127.0.0.1:5000/api/2.0/mlflow/runs/search"
    data = json.dumps({"experiment_ids": ["0"]}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"MLflow API responded with status {response.status}"
            resp_data = json.loads(response.read().decode('utf-8'))
    except URLError as e:
        raise AssertionError(f"Failed to connect to MLflow server at 127.0.0.1:5000. Is it running? Error: {e}")

    runs = resp_data.get("runs", [])
    assert len(runs) > 0, "No MLflow runs found in experiment 0"

    run = runs[0]
    run_data = run.get('data', {})

    params = {p['key']: p['value'] for p in run_data.get('params', [])}
    metrics = {m['key']: m['value'] for m in run_data.get('metrics', [])}

    assert 'smoothing_weight' in params, "Parameter 'smoothing_weight' not logged in MLflow"
    assert params['smoothing_weight'] in ['15', '15.0'], \
        f"Incorrect smoothing_weight logged. Expected 15, got {params['smoothing_weight']}"

    assert 'global_mean_price' in metrics, "Metric 'global_mean_price' not logged in MLflow"
    assert abs(metrics['global_mean_price'] - 727000.0) < 0.1, \
        f"Incorrect global_mean_price logged. Expected ~727000.0, got {metrics['global_mean_price']}"