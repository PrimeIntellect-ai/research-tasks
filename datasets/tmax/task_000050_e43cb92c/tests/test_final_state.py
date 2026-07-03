# test_final_state.py
import json
import os
import pytest

def test_accuracy_meets_threshold():
    truth_path = "/app/ground_truth.json"
    results_path = "/home/user/results.json"

    assert os.path.exists(truth_path), f"Ground truth file missing at {truth_path}"
    assert os.path.exists(results_path), f"Results file missing at {results_path}"

    with open(truth_path, 'r') as f:
        truth = json.load(f)

    try:
        with open(results_path, 'r') as f:
            preds = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not read or parse {results_path}: {e}")

    correct = 0
    for k, v in truth.items():
        if str(preds.get(k, -1)) == str(v):
            correct += 1

    accuracy = correct / len(truth) if truth else 0.0

    assert accuracy >= 0.95, f"Accuracy {accuracy:.4f} is below the required threshold of 0.95"