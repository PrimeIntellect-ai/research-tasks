# test_final_state.py
import json
import os
import pytest

def test_recovered_logs_accuracy():
    truth_file = '/app/.hidden/true_logs.json'
    pred_file = '/home/user/recovered_logs.json'

    assert os.path.isfile(truth_file), f"Truth file missing: {truth_file}"
    assert os.path.isfile(pred_file), f"Student output missing: {pred_file}"

    with open(truth_file, 'r') as f:
        try:
            truth = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON from {truth_file}")

    with open(pred_file, 'r') as f:
        try:
            pred = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON from {pred_file}")

    assert isinstance(truth, list), "Truth data should be a JSON array"
    assert isinstance(pred, list), "Student output should be a JSON array"

    truth_dict = {f"{r.get('ip', '')}|{r.get('timestamp', '')}": r for r in truth}
    pred_dict = {f"{r.get('ip', '')}|{r.get('timestamp', '')}": r for r in pred}

    correct = 0
    for k, v in truth_dict.items():
        if k in pred_dict and pred_dict[k] == v:
            correct += 1

    total = len(truth_dict)
    assert total > 0, "Truth data is empty"

    accuracy = correct / total
    threshold = 0.95

    assert accuracy >= threshold, f"Accuracy {accuracy:.4f} is below the threshold of {threshold}. {correct}/{total} correct records."