# test_final_state.py

import os
import pandas as pd
import pytest

def test_predictions_file_exists():
    pred_path = '/home/user/predictions.csv'
    assert os.path.isfile(pred_path), f"Predictions file is missing at {pred_path}"

def test_predictions_accuracy():
    pred_path = '/home/user/predictions.csv'
    truth_path = '/tmp/hidden_test_labels.csv'

    assert os.path.isfile(pred_path), f"Missing {pred_path}"
    assert os.path.isfile(truth_path), f"Missing {truth_path}"

    try:
        pred = pd.read_csv(pred_path)
    except Exception as e:
        pytest.fail(f"Failed to read {pred_path}: {e}")

    try:
        truth = pd.read_csv(truth_path)
    except Exception as e:
        pytest.fail(f"Failed to read {truth_path}: {e}")

    assert 'user_id' in pred.columns, "Predictions file must contain 'user_id' column"
    assert 'prediction' in pred.columns, "Predictions file must contain 'prediction' column"

    merged = pd.merge(truth, pred, on='user_id')
    assert len(merged) > 0, "No matching user_ids found between predictions and truth"

    accuracy = (merged['label'] == merged['prediction']).mean()

    assert accuracy >= 0.85, f"Accuracy {accuracy:.4f} is less than the required threshold of 0.85"

def test_rapidcsv_fixed():
    header_path = '/app/rapidcsv/src/rapidcsv.h'
    assert os.path.isfile(header_path), f"Vendored rapidcsv header is missing at {header_path}"

    with open(header_path, 'r') as f:
        content = f.read()

    # The agent should have changed the default separator back to ','
    # Check that '|' is not used as the default separator in SeparatorParams
    assert "explicit SeparatorParams(const char pSeparator = '|'" not in content, \
        "The rapidcsv default separator was not fixed from '|' to ','"