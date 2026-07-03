# test_final_state.py

import os
import json
import pytest

def canonicalize(cycle):
    return tuple(sorted(str(x) for x in cycle))

def test_deadlocks_json_exists():
    output_path = "/home/user/deadlocks.json"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

def test_deadlocks_f1_score():
    output_path = "/home/user/deadlocks.json"
    ground_truth_path = "/tmp/ground_truth.json"

    assert os.path.isfile(output_path), f"Output file missing: {output_path}"
    assert os.path.isfile(ground_truth_path), f"Ground truth file missing: {ground_truth_path}"

    with open(output_path, "r") as f:
        try:
            pred_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not a valid JSON.")

    assert isinstance(pred_data, list), f"Expected JSON to contain a list of lists, got {type(pred_data)}"
    pred_cycles = set(canonicalize(c) for c in pred_data)

    with open(ground_truth_path, "r") as f:
        true_data = json.load(f)
    true_cycles = set(canonicalize(c) for c in true_data)

    tp = len(pred_cycles & true_cycles)
    fp = len(pred_cycles - true_cycles)
    fn = len(true_cycles - pred_cycles)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.99, f"F1 Score of identified cycles is {f1:.4f}, expected >= 0.99. True Positives: {tp}, False Positives: {fp}, False Negatives: {fn}."