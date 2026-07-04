# test_final_state.py

import os
import json
import math
import subprocess
import pytest

def test_run_sh_exists_and_executable():
    run_script = '/home/user/run.sh'
    assert os.path.isfile(run_script), f"{run_script} does not exist."
    assert os.access(run_script, os.X_OK), f"{run_script} is not executable."

def test_pipeline_py_exists():
    assert os.path.isfile('/home/user/pipeline.py'), "/home/user/pipeline.py does not exist."

def test_run_sh_environment_variables():
    run_script = '/home/user/run.sh'
    with open(run_script, 'r') as f:
        content = f.read()

    expected_exports = [
        "PYTHONHASHSEED=42",
        "OMP_NUM_THREADS=1",
        "OPENBLAS_NUM_THREADS=1",
        "MKL_NUM_THREADS=1"
    ]
    for exp in expected_exports:
        assert exp in content.replace(" ", "").replace('"', '').replace("'", ""), f"Expected export {exp} not found in run.sh."

def test_processed_data_exists():
    h5_file = '/home/user/processed_data/clean_data.h5'
    assert os.path.isfile(h5_file), f"{h5_file} does not exist."

def test_metrics_json_exists_and_content():
    metrics_file = '/home/user/metrics.json'
    assert os.path.isfile(metrics_file), f"{metrics_file} does not exist."

    with open(metrics_file, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not a valid JSON file.")

    assert "mse" in metrics, "Key 'mse' missing in metrics.json"
    assert "coef_sum" in metrics, "Key 'coef_sum' missing in metrics.json"

    # We don't strictly recompute the model here to avoid sklearn dependency in standard library test,
    # but we can verify they are floats.
    assert isinstance(metrics["mse"], (int, float)), "MSE should be a number."
    assert isinstance(metrics["coef_sum"], (int, float)), "coef_sum should be a number."