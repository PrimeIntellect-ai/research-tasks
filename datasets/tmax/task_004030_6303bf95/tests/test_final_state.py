# test_final_state.py
import os
import json
import math
import pytest

def test_venv_exists():
    venv_path = '/home/user/venv'
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} does not exist."

    # Check for python executable in venv
    bin_path = os.path.join(venv_path, 'bin', 'python')
    if not os.path.exists(bin_path):
        bin_path = os.path.join(venv_path, 'Scripts', 'python.exe') # fallback for windows-like structures, though path is unix
    assert os.path.isfile(bin_path), f"Python executable not found in virtual environment at {bin_path}."

def test_pipeline_script_content():
    pipeline_path = '/home/user/experiment/pipeline.py'
    assert os.path.isfile(pipeline_path), f"The script {pipeline_path} is missing."

    with open(pipeline_path, 'r') as f:
        content = f.read()

    assert "GaussianNB" in content, "The script does not use GaussianNB as required."
    assert "Pipeline" in content, "The script does not use sklearn.pipeline.Pipeline to fix the data leak."
    assert "RandomForestClassifier" not in content, "The script still contains RandomForestClassifier instead of GaussianNB."

def test_final_metrics_json():
    metrics_path = '/home/user/experiment/artifacts/final_metrics.json'
    assert os.path.isfile(metrics_path), f"The metrics file {metrics_path} is missing."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {metrics_path} does not contain valid JSON.")

    assert "accuracy" in metrics, "The JSON file does not contain the 'accuracy' key."

    accuracy = metrics["accuracy"]
    assert isinstance(accuracy, (int, float)), "The accuracy value should be a number."

    expected_accuracy = 0.81
    assert math.isclose(accuracy, expected_accuracy, rel_tol=1e-2), \
        f"Expected accuracy to be approximately {expected_accuracy}, but got {accuracy}. Check if the data leak was properly fixed and the correct model was used."