# test_final_state.py

import os
import pytest

def test_f1_score_motif_matches():
    pred_path = '/home/user/motif_matches.csv'
    truth_path = '/app/ground_truth_indices.txt'

    assert os.path.exists(pred_path), f"Output file {pred_path} does not exist."
    assert os.path.exists(truth_path), f"Ground truth file {truth_path} does not exist."

    try:
        with open(pred_path, 'r') as f:
            preds = set(int(x.strip()) for x in f if x.strip())
    except ValueError:
        pytest.fail(f"File {pred_path} contains non-integer values.")

    with open(truth_path, 'r') as f:
        truths = set(int(x.strip()) for x in f if x.strip())

    if not preds:
        pytest.fail("Predicted indices file is empty or contains no valid indices. F1 Score: 0.0")

    tp = len(preds & truths)
    fp = len(preds - truths)
    fn = len(truths - preds)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.85, f"F1 Score {f1:.4f} is below the threshold of 0.85. TP: {tp}, FP: {fp}, FN: {fn}"