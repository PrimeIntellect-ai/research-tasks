# test_final_state.py

import os
import glob
import math
import hashlib
import pytest

def get_expected_metrics():
    # Read model parameters
    params_path = '/home/user/model_params.txt'
    if not os.path.exists(params_path):
        pytest.fail(f"Missing {params_path}")

    params = {}
    with open(params_path, 'r') as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=')
                params[k] = float(v)

    w_a = params.get('weight_A', 1.5)
    w_b = params.get('weight_B', -0.5)
    bias = params.get('bias', 2.0)

    preds = []
    actuals = []

    csv_files = glob.glob('/home/user/data/*.csv')
    if not csv_files:
        pytest.fail("No CSV files found in /home/user/data/")

    for filename in csv_files:
        with open(filename, 'r') as f:
            header = f.readline()
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                a, b, actual = float(parts[0]), float(parts[1]), float(parts[2])
                pred = w_a * a + w_b * b + bias
                preds.append(pred)
                actuals.append(actual)

    n = len(preds)
    if n < 2:
        pytest.fail("Not enough data to calculate statistics")

    mean_pred = sum(preds) / n
    mean_actual = sum(actuals) / n

    cov = sum((preds[i] - mean_pred) * (actuals[i] - mean_actual) for i in range(n)) / (n - 1)

    var_pred = sum((preds[i] - mean_pred)**2 for i in range(n)) / (n - 1)
    var_actual = sum((actuals[i] - mean_actual)**2 for i in range(n)) / (n - 1)

    corr = cov / math.sqrt(var_pred * var_actual)

    return cov, corr

def test_process_script_exists_and_executable():
    script_path = '/home/user/process.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_metrics_file():
    metrics_path = '/home/user/metrics.txt'
    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} does not exist"

    cov, corr = get_expected_metrics()
    expected_cov_str = f"Covariance: {cov:.4f}"
    expected_corr_str = f"Correlation: {corr:.4f}"

    with open(metrics_path, 'r') as f:
        content = f.read().strip()

    assert expected_cov_str in content, f"Expected '{expected_cov_str}' not found in {metrics_path}. Content:\n{content}"
    assert expected_corr_str in content, f"Expected '{expected_corr_str}' not found in {metrics_path}. Content:\n{content}"

def test_reproducibility_file():
    metrics_path = '/home/user/metrics.txt'
    repro_path = '/home/user/reproducibility.txt'

    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} does not exist"
    assert os.path.isfile(repro_path), f"Reproducibility file {repro_path} does not exist"

    with open(metrics_path, 'rb') as f:
        metrics_content = f.read()
    expected_md5 = hashlib.md5(metrics_content).hexdigest()

    with open(repro_path, 'r') as f:
        repro_content = f.read().strip()

    assert expected_md5 in repro_content, f"MD5 hash {expected_md5} not found in {repro_path}. Content:\n{repro_content}"