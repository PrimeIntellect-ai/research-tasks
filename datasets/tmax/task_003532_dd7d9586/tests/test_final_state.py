# test_final_state.py
import os
import json
import urllib.request
import urllib.error

def test_mlflow_server_and_experiment():
    url = "http://127.0.0.1:5000/api/2.0/mlflow/experiments/get-by-name?experiment_name=Wear_Prediction"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            assert "experiment" in data, "Experiment 'Wear_Prediction' not found in MLflow response."
            assert data["experiment"]["name"] == "Wear_Prediction", "Experiment name does not match 'Wear_Prediction'."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to MLflow server at http://127.0.0.1:5000. Is it running? Error: {e}"
    except Exception as e:
        assert False, f"An unexpected error occurred while querying MLflow: {e}"

def test_best_run_file_exists_and_format():
    filepath = "/home/user/best_run.json"
    assert os.path.exists(filepath), f"Missing file: {filepath}"
    assert os.path.isfile(filepath), f"Not a file: {filepath}"

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {filepath} is not valid JSON."

    assert "best_alpha" in data, f"Key 'best_alpha' missing in {filepath}"
    assert "best_cv_r2" in data, f"Key 'best_cv_r2' missing in {filepath}"

    assert isinstance(data["best_alpha"], (int, float)), "Value for 'best_alpha' must be a float."
    assert isinstance(data["best_cv_r2"], (int, float)), "Value for 'best_cv_r2' must be a float."

def test_best_run_values():
    filepath = "/home/user/best_run.json"
    if not os.path.exists(filepath):
        return # Handled by previous test

    with open(filepath, "r") as f:
        data = json.load(f)

    best_alpha = float(data["best_alpha"])
    best_cv_r2 = float(data["best_cv_r2"])

    # Based on the underlying data and Ridge regression with GroupKFold
    expected_alpha = 0.1
    expected_cv_r2 = 0.9619

    assert best_alpha == expected_alpha, f"Expected best_alpha to be {expected_alpha}, but got {best_alpha}"
    assert abs(best_cv_r2 - expected_cv_r2) < 0.001, f"Expected best_cv_r2 to be approximately {expected_cv_r2}, but got {best_cv_r2}"