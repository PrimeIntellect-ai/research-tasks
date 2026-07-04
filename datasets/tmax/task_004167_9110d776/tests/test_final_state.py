# test_final_state.py

import os
import pytest
import pandas as pd
from sklearn.metrics import mean_squared_error

def test_predictions_exist():
    preds_path = "/app/linreg_pipeline/predictions.csv"
    assert os.path.isfile(preds_path), f"The predictions file {preds_path} does not exist. Did you run the pipeline?"

def test_mse_threshold():
    preds_path = "/app/linreg_pipeline/predictions.csv"
    targets_path = "/app/data/test_targets_hidden.csv"

    assert os.path.isfile(preds_path), f"Missing predictions file: {preds_path}"
    assert os.path.isfile(targets_path), f"Missing hidden targets file: {targets_path}"

    try:
        preds_df = pd.read_csv(preds_path)
    except Exception as e:
        pytest.fail(f"Failed to read predictions CSV: {e}")

    try:
        targets_df = pd.read_csv(targets_path)
    except Exception as e:
        pytest.fail(f"Failed to read hidden targets CSV: {e}")

    # Assume the predictions and targets are in the first column or aligned
    # We will just take the last column if there are multiple, or the only column.
    # Usually, predictions is a single column.
    preds_vals = preds_df.iloc[:, -1].values
    targets_vals = targets_df.iloc[:, -1].values

    assert len(preds_vals) == len(targets_vals), (
        f"Length mismatch: predictions has {len(preds_vals)} rows, "
        f"but targets has {len(targets_vals)} rows."
    )

    mse = mean_squared_error(targets_vals, preds_vals)
    threshold = 0.5

    assert mse <= threshold, (
        f"Mean Squared Error is too high! "
        f"Expected MSE <= {threshold}, but got {mse:.4f}. "
        f"The bug in the data pipeline might not be fully fixed."
    )