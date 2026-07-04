# test_final_state.py

import os
import subprocess
import urllib.request
import json
import pytest

def test_train_csv_exists():
    assert os.path.isfile('/home/user/train.csv'), "/home/user/train.csv is missing. The data was not downloaded correctly."

def test_model_pkl_exists():
    assert os.path.isfile('/home/user/model.pkl'), "/home/user/model.pkl is missing. The model was not saved."

def test_predict_script_exists():
    assert os.path.isfile('/home/user/predict.py'), "/home/user/predict.py is missing."

def test_predict_mse_threshold():
    try:
        result = subprocess.run(
            ['python3', '/home/user/predict.py', '/app/test_secret.csv'],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing predict.py failed with error:\n{e.stderr}")

    output = result.stdout.strip().split('\n')
    assert len(output) > 0, "predict.py produced no output."

    last_line = output[-1].strip()
    try:
        mse = float(last_line)
    except ValueError:
        pytest.fail(f"Could not parse the last line of output as a float. Output was: {last_line}")

    assert mse <= 45.0, f"MSE {mse} is not <= 45.0. Model performance is inadequate."

def test_mlflow_tracking():
    try:
        # Get experiment by name
        url = 'http://localhost:5000/api/2.0/mlflow/experiments/get-by-name?experiment_name=Support_Analysis'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            exp_data = json.loads(response.read().decode())

        assert 'experiment' in exp_data, "Experiment 'Support_Analysis' not found in MLflow."
        exp_id = exp_data['experiment']['experiment_id']

        # Search runs in the experiment
        search_url = 'http://localhost:5000/api/2.0/mlflow/runs/search'
        search_payload = json.dumps({"experiment_ids": [exp_id]}).encode('utf-8')
        req2 = urllib.request.Request(search_url, data=search_payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req2) as response:
            runs_data = json.loads(response.read().decode())

        runs = runs_data.get('runs', [])
        assert len(runs) > 0, "No runs found in the 'Support_Analysis' experiment."

        # Check metrics in the latest run
        metrics = runs[0].get('data', {}).get('metrics', [])
        metric_keys = [m['key'] for m in metrics]

        # We expect correlation metrics for the 3 features
        assert len(metrics) >= 3, f"Expected at least 3 metrics logged, found {len(metrics)}. Keys: {metric_keys}"

    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to MLflow server: {e}")
    except Exception as e:
        pytest.fail(f"MLflow validation failed: {e}")