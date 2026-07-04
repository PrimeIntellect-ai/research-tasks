# test_final_state.py

import os
import csv
import json
import urllib.request
import urllib.parse
import urllib.error
import pytest

def test_cleaned_data_csv():
    path = "/home/user/cleaned_data.csv"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        assert headers is not None, "cleaned_data.csv is empty or missing headers."
        assert 'group_id' in headers, "Missing group_id column in cleaned_data.csv"
        assert 'group_hash' in headers, "Missing group_hash column in cleaned_data.csv"

        for row_idx, row in enumerate(reader):
            group_id_str = row['group_id']
            group_hash_str = row['group_hash']

            assert group_id_str != "", f"Row {row_idx} has missing group_id."
            assert group_hash_str != "", f"Row {row_idx} has missing group_hash."

            # They should be integers (or float representations of integers like "2.0" which need handling, 
            # but the task says ensure group_id is represented as an integer dtype, so it should be "2" not "2.0")
            try:
                # If it's saved as an integer dtype, it should parse as int directly.
                # Let's be slightly lenient if they saved floats, but strict on the bitwise logic.
                group_id_val = int(float(group_id_str))
                group_hash_val = int(float(group_hash_str))
            except ValueError:
                pytest.fail(f"Row {row_idx} has non-numeric group_id or group_hash.")

            assert group_hash_val == (group_id_val << 1), f"Row {row_idx}: group_hash ({group_hash_val}) != group_id ({group_id_val}) << 1"


def test_mlflow_experiment_and_run():
    # Check MLflow API
    base_url = "http://127.0.0.1:5000/api/2.0/mlflow"

    # 1. Get experiment by name
    exp_name = "Data_Cleaning_Exp"
    params = urllib.parse.urlencode({'experiment_name': exp_name})
    get_exp_url = f"{base_url}/experiments/get-by-name?{params}"

    try:
        req = urllib.request.Request(get_exp_url)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to MLflow server or experiment not found: {e}")

    assert 'experiment' in res_data, "MLflow response missing 'experiment' data."
    exp_id = res_data['experiment']['experiment_id']

    # 2. Search runs
    search_url = f"{base_url}/runs/search"
    search_payload = json.dumps({'experiment_ids': [exp_id]}).encode('utf-8')
    req = urllib.request.Request(search_url, data=search_payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as response:
            runs_data = json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to search MLflow runs: {e}")

    runs = runs_data.get('runs', [])
    assert len(runs) > 0, "No runs found in the MLflow experiment."

    run = runs[0]
    run_data = run.get('data', {})

    metrics = {m['key']: m['value'] for m in run_data.get('metrics', [])}
    params = {p['key']: p['value'] for p in run_data.get('params', [])}

    assert 'accuracy' in metrics, "Metric 'accuracy' was not logged to MLflow."
    assert 'n_components' in params, "Parameter 'n_components' was not logged to MLflow."
    assert params['n_components'] in ('2', 2), f"Expected n_components to be 2, got {params['n_components']}"