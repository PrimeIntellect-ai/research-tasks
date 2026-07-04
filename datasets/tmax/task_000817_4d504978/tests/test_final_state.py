# test_final_state.py

import os
import pandas as pd
import pytest

def test_audit_results_accuracy():
    pred_path = '/home/user/audit_results.csv'
    truth_path = '/tmp/expected_results.csv'

    assert os.path.isfile(pred_path), f"Output file {pred_path} is missing. The auditing tool did not produce the expected output file."
    assert os.path.isfile(truth_path), f"Truth file {truth_path} is missing. The environment setup is corrupted."

    try:
        pred = pd.read_csv(pred_path).set_index('Port')
    except Exception as e:
        pytest.fail(f"Failed to read {pred_path} as a CSV: {e}")

    try:
        truth = pd.read_csv(truth_path).set_index('Port')
    except Exception as e:
        pytest.fail(f"Failed to read {truth_path} as a CSV: {e}")

    # Ensure column 'Status' exists in the prediction
    assert 'Status' in pred.columns, f"Expected column 'Status' not found in {pred_path}."

    joined = truth.join(pred, lsuffix='_truth', rsuffix='_pred')
    accuracy = (joined['Status_truth'] == joined['Status_pred']).mean()

    assert accuracy >= 0.95, f"Accuracy {accuracy:.4f} is below the required threshold of 0.95."