# test_final_state.py

import os
import stat
import json
import csv
import re

def test_run_pipeline_script_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"Bash script not found at {script_path}"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {script_path} is not executable"

def test_virtual_environment_exists():
    python_path = '/home/user/venv/bin/python'
    assert os.path.isfile(python_path) or os.path.isfile('/home/user/venv/bin/python3'), "Virtual environment python executable not found in /home/user/venv"

def test_predict_script_exists():
    script_path = '/home/user/predict.py'
    assert os.path.isfile(script_path), f"Python script not found at {script_path}"

def test_predictions_correct():
    dataset_path = '/home/user/dataset.csv'
    weights_path = '/home/user/weights.json'
    predictions_path = '/home/user/predictions.csv'

    assert os.path.isfile(predictions_path), f"Predictions file not found at {predictions_path}"

    with open(weights_path, 'r') as f:
        w_data = json.load(f)
    weights = w_data['weights']
    bias = w_data['bias']

    expected_preds = {}
    with open(dataset_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            score = (float(row['f1']) * weights[0] +
                     float(row['f2']) * weights[1] +
                     float(row['f3']) * weights[2] +
                     float(row['f4']) * weights[3] + bias)
            pred = 1 if score > 0 else 0
            expected_preds[row['id']] = str(pred)

    actual_preds = {}
    with open(predictions_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['id', 'prediction'], f"Incorrect header in predictions.csv: {header}"
        for row in reader:
            if not row:
                continue
            actual_preds[row[0]] = row[1]

    assert len(actual_preds) == len(expected_preds), f"Expected {len(expected_preds)} predictions, found {len(actual_preds)}"

    for pid, expected_pred in expected_preds.items():
        assert pid in actual_preds, f"Prediction for id {pid} missing"
        assert actual_preds[pid] == expected_pred, f"Incorrect prediction for id {pid}: expected {expected_pred}, got {actual_preds[pid]}"

def test_metrics_log():
    metrics_path = '/home/user/metrics.txt'
    assert os.path.isfile(metrics_path), f"Metrics log not found at {metrics_path}"

    with open(metrics_path, 'r') as f:
        content = f.read()

    match = re.search(r'inference_time_ms:\d+(\.\d+)?', content)
    assert match is not None, f"Metrics log does not contain the correct format 'inference_time_ms:<time_in_milliseconds>'. Content: {content}"