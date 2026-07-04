# test_final_state.py

import os
import csv
import pytest

def test_predictions_generated():
    """Verify that the predictions.csv file was generated."""
    path = "/home/user/predictions.csv"
    assert os.path.isfile(path), f"Missing file: {path}. Did you run the pipeline script?"

def test_model_accuracy():
    """Verify that the accuracy on the test set is above 0.85, indicating the bug was fixed."""
    preds_path = "/home/user/predictions.csv"
    truths_path = "/home/user/data/test_labels.csv"

    assert os.path.isfile(preds_path), f"Cannot calculate accuracy, missing {preds_path}"
    assert os.path.isfile(truths_path), f"Cannot calculate accuracy, missing {truths_path}"

    with open(preds_path, 'r') as f:
        reader = csv.DictReader(f)
        try:
            preds = [int(float(row['prediction'])) for row in reader]
        except KeyError:
            pytest.fail("predictions.csv is missing the 'prediction' column.")

    with open(truths_path, 'r') as f:
        reader = csv.DictReader(f)
        truths = [int(float(row['target'])) for row in reader]

    assert len(preds) == len(truths), f"Expected {len(truths)} predictions, but got {len(preds)}."

    correct = sum(1 for p, t in zip(preds, truths) if p == t)
    accuracy = correct / len(truths)

    assert accuracy > 0.85, f"Accuracy too low: {accuracy:.4f}. The precision bug was not properly fixed."