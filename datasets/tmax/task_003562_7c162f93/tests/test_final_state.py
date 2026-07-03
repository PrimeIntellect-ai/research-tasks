# test_final_state.py

import os
import json
import math

def test_metrics_json_correct():
    metrics_file = '/home/user/metrics.json'
    assert os.path.exists(metrics_file), f"{metrics_file} does not exist. Did you run the script?"

    with open(metrics_file, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{metrics_file} contains invalid JSON."

    assert 'test_feature1_mean' in metrics, "Key 'test_feature1_mean' not found in metrics.json."

    val = metrics['test_feature1_mean']
    expected = -0.19833621453265008

    assert math.isclose(val, expected, abs_tol=1e-5), (
        f"Expected test_feature1_mean to be approx {expected}, but got {val}. "
        "Make sure you split the data FIRST, then fit the scaler ONLY on the training set."
    )

def test_clean_data_script_exists():
    script_file = '/home/user/clean_data.py'
    assert os.path.exists(script_file), f"{script_file} does not exist."
    assert os.path.isfile(script_file), f"{script_file} is not a file."