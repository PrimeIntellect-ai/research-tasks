# test_final_state.py

import os
import stat
import pandas as pd
import pytest

def test_vmath_executable_exists():
    path = "/app/vmath-1.2/vmath"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile the tool?"

    # Check if it's executable
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_evaluate_script_exists():
    path = "/home/user/evaluate.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."

def test_predictions_csv_exists():
    path = "/home/user/predictions.csv"
    assert os.path.isfile(path), f"Predictions file {path} does not exist. Did you run your script?"

def test_prediction_accuracy():
    predictions_path = "/home/user/predictions.csv"
    truth_path = "/app/ground_truth.csv"

    assert os.path.isfile(predictions_path), f"Predictions file {predictions_path} is missing."
    assert os.path.isfile(truth_path), f"Ground truth file {truth_path} is missing."

    try:
        truth = pd.read_csv(truth_path)
        preds = pd.read_csv(predictions_path)
    except Exception as e:
        pytest.fail(f"Failed to read CSV files: {e}")

    assert 'experiment_id' in preds.columns, "Predictions file must have an 'experiment_id' column."
    assert 'predicted_class' in preds.columns, "Predictions file must have a 'predicted_class' column."

    merged = pd.merge(truth, preds, on='experiment_id')
    assert len(merged) > 0, "No matching experiment_ids found between predictions and ground truth."
    assert len(merged) == len(truth), f"Expected {len(truth)} predictions, but got {len(merged)} matching rows."

    accuracy = (merged['true_class'] == merged['predicted_class']).mean()

    assert accuracy >= 0.95, f"Accuracy is {accuracy:.4f}, which is below the threshold of 0.95."