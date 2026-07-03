# test_final_state.py

import os
import json
import subprocess
import pytest

def test_yq_installed_and_fixed():
    """Check if the yq package was installed successfully and is executable."""
    try:
        result = subprocess.run(["yq", "--version"], capture_output=True, text=True)
        assert result.returncode == 0, f"yq command failed with output: {result.stderr}"
    except FileNotFoundError:
        pytest.fail("yq command not found. The package was likely not installed correctly.")

def test_script_exists():
    """Check if the required bash script was created."""
    script_path = "/home/user/audit_cycles.sh"
    assert os.path.isfile(script_path), f"Script file is missing at {script_path}"

def test_suspects_json_f1_score():
    """Calculate the F1 score of the extracted accounts against the ground truth."""
    pred_file = "/home/user/suspects.json"
    truth_file = "/tmp/ground_truth.json"

    assert os.path.isfile(pred_file), f"Output file is missing at {pred_file}"
    assert os.path.isfile(truth_file), f"Ground truth file is missing at {truth_file}"

    try:
        with open(pred_file) as f:
            preds_data = json.load(f)
            assert isinstance(preds_data, list), "Output must be a JSON array"
            preds = set(preds_data)
    except json.JSONDecodeError:
        pytest.fail(f"Output file {pred_file} does not contain valid JSON.")

    with open(truth_file) as f:
        truths = set(json.load(f))

    tp = len(preds & truths)
    fp = len(preds - truths)
    fn = len(truths - preds)

    if tp == 0:
        f1 = 0.0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 Score is {f1:.4f}, which is below the threshold of 0.95. True Positives: {tp}, False Positives: {fp}, False Negatives: {fn}."