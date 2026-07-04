# test_final_state.py
import os
import json
import subprocess
import math

def test_c_source_exists():
    assert os.path.isfile("/home/user/linear_regression.c"), "C program /home/user/linear_regression.c does not exist."

def test_evaluate_script_exists_and_executable():
    script_path = "/home/user/evaluate.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."

def test_evaluate_script_runs_and_creates_json():
    script_path = "/home/user/evaluate.sh"
    json_path = "/home/user/model_metrics.json"

    # Remove the JSON file if it exists to ensure the script creates it
    if os.path.exists(json_path):
        os.remove(json_path)

    result = subprocess.run([script_path], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"evaluate.sh failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(json_path), f"JSON file {json_path} was not created by the script."

def test_json_content():
    json_path = "/home/user/model_metrics.json"
    assert os.path.isfile(json_path), f"JSON file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} does not contain valid JSON."

    assert "model" in data, "Key 'model' missing in JSON."
    assert data["model"] == "linear_regression", f"Expected model name 'linear_regression', got {data['model']}"

    assert "parameters" in data, "Key 'parameters' missing in JSON."
    assert "slope" in data["parameters"], "Key 'slope' missing in parameters."
    assert "intercept" in data["parameters"], "Key 'intercept' missing in parameters."

    assert "evaluation" in data, "Key 'evaluation' missing in JSON."
    assert "mse" in data["evaluation"], "Key 'mse' missing in evaluation."

    slope = float(data["parameters"]["slope"])
    intercept = float(data["parameters"]["intercept"])
    mse = float(data["evaluation"]["mse"])

    assert math.isclose(slope, 2.01, abs_tol=1e-3), f"Expected slope around 2.01, got {slope}"
    assert math.isclose(intercept, 0.03, abs_tol=1e-3), f"Expected intercept around 0.03, got {intercept}"
    assert math.isclose(mse, 0.0102, abs_tol=1e-3), f"Expected mse around 0.0102, got {mse}"