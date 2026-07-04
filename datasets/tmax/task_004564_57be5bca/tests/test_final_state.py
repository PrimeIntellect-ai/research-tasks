# test_final_state.py

import os
import pandas as pd
from sklearn.metrics import r2_score

def test_predictions_file_exists():
    assert os.path.isfile("/home/user/pipeline/predictions.csv"), "The predictions file /home/user/pipeline/predictions.csv does not exist."

def test_predictions_format_and_metric():
    preds_path = "/home/user/pipeline/predictions.csv"
    truth_path = "/app/data/.hidden_val_target.csv"

    assert os.path.isfile(preds_path), f"File not found: {preds_path}"
    assert os.path.isfile(truth_path), f"File not found: {truth_path}"

    try:
        preds = pd.read_csv(preds_path)
    except Exception as e:
        assert False, f"Failed to read {preds_path} as CSV: {e}"

    try:
        truth = pd.read_csv(truth_path)
    except Exception as e:
        assert False, f"Failed to read {truth_path} as CSV: {e}"

    assert 'predicted_target' in preds.columns, "The predictions file must contain a column named 'predicted_target'."
    assert 'target' in truth.columns, "The truth file is missing the 'target' column."

    # Ensure lengths match
    assert len(preds) == len(truth), f"Number of predictions ({len(preds)}) does not match number of validation samples ({len(truth)})."

    # Calculate R2 score
    score = r2_score(truth['target'], preds['predicted_target'])

    # Assert against the threshold
    assert score >= 0.75, f"R2 score {score:.4f} is below the required threshold of 0.75."