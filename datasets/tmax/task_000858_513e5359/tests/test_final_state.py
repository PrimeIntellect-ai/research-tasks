# test_final_state.py
import os
import numpy as np
import pytest

def test_final_state():
    # 1. Check if the required files and directories exist
    train_data_path = "/home/user/train_data.csv"
    ml_pipeline_dir = "/home/user/ml_pipeline"
    predictions_path = "/home/user/predictions.txt"

    assert os.path.exists(train_data_path), f"Missing parsed training data at {train_data_path}"
    assert os.path.isfile(train_data_path), f"{train_data_path} is not a file"

    assert os.path.exists(ml_pipeline_dir), f"Missing Rust project directory at {ml_pipeline_dir}"
    assert os.path.isdir(ml_pipeline_dir), f"{ml_pipeline_dir} is not a directory"

    assert os.path.exists(predictions_path), f"Missing predictions file at {predictions_path}"
    assert os.path.isfile(predictions_path), f"{predictions_path} is not a file"

    # 2. Evaluate the predictions
    try:
        preds = np.loadtxt(predictions_path)
    except Exception as e:
        pytest.fail(f"Failed to load predictions from {predictions_path}: {e}")

    # Ensure it's a 1D array
    if preds.ndim == 0:
        preds = np.array([preds])
    elif preds.ndim > 1:
        preds = preds.flatten()

    targets = np.array([6.3, 12.75, -1.9, 19.2, 4.0])

    assert len(preds) == len(targets), f"Length mismatch: predicted {len(preds)} values, expected {len(targets)}"

    mse = np.mean((preds - targets) ** 2)
    threshold = 2.0

    assert mse <= threshold, f"MSE too high: {mse} (must be <= {threshold})"