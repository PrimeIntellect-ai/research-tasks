# test_final_state.py

import os
import subprocess
import re
import pytest

def test_prepare_data_script_exists_and_runs():
    script_path = "/home/user/prepare_data.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path} must exist."

    # Run the script to ensure reproducibility
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed to execute.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_model_accuracy_threshold():
    csv_path = "/home/user/train_clean.csv"
    assert os.path.isfile(csv_path), f"Output dataset missing: {csv_path} was not generated."

    evaluator_path = "/app/model_evaluator"
    assert os.path.isfile(evaluator_path), f"Model evaluator missing: {evaluator_path}"
    assert os.access(evaluator_path, os.X_OK), f"Model evaluator {evaluator_path} is not executable."

    # Evaluate the generated dataset
    result = subprocess.run([evaluator_path, csv_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Model evaluator failed to run on {csv_path}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Extract accuracy using regex (equivalent to grep -oP 'ACCURACY=\K[0-9.]+')
    match = re.search(r'ACCURACY=([0-9.]+)', result.stdout)
    assert match is not None, f"Could not extract ACCURACY from the evaluator output.\nOutput was: {result.stdout}"

    accuracy = float(match.group(1))
    threshold = 0.85
    assert accuracy >= threshold, f"Extracted accuracy {accuracy} is strictly less than the required threshold {threshold}."