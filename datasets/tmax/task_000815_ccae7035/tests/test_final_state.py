# test_final_state.py
import os
import numpy as np
import pytest

def test_predictions_accuracy():
    predictions_path = '/home/user/predictions.csv'
    truth_path = '/app/test_labels.csv'

    assert os.path.isfile(predictions_path), f"Expected predictions file at {predictions_path} does not exist."
    assert os.path.isfile(truth_path), f"Expected truth file at {truth_path} does not exist."

    try:
        expected = np.loadtxt(truth_path, dtype=int)
    except Exception as e:
        pytest.fail(f"Failed to load truth labels: {e}")

    try:
        actual = np.loadtxt(predictions_path, dtype=int)
    except Exception as e:
        pytest.fail(f"Failed to load predictions: {e}")

    assert len(expected) == len(actual), f"Length mismatch: expected {len(expected)} predictions, got {len(actual)}"

    accuracy = np.mean(expected == actual)
    threshold = 0.85

    assert accuracy >= threshold, f"Accuracy {accuracy:.4f} is below the required threshold of {threshold}"