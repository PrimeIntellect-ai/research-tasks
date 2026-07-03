# test_final_state.py

import os
import pandas as pd
import pytest

def load_data(path):
    if not os.path.exists(path):
        return set()
    try:
        df = pd.read_csv(path, header=None, names=['user_id', 'timestamp'])
        # Drop any rows with NaN values that might occur from trailing commas or malformed lines
        df = df.dropna()
        return set(tuple(x) for x in df.to_numpy())
    except Exception:
        return set()

def test_audit_files_exist():
    """Verify that the user created the C file, compiled it, and generated the output."""
    assert os.path.isfile('/home/user/audit.c'), "Source code /home/user/audit.c is missing."
    assert os.path.isfile('/home/user/audit'), "Compiled binary /home/user/audit is missing."
    assert os.path.isfile('/home/user/flagged.csv'), "Output file /home/user/flagged.csv is missing."

def test_f1_score_metric():
    """Evaluate the F1 score of the flagged users against the ground truth with a +/- 1 second tolerance."""
    truth_path = '/app/ground_truth.csv'
    preds_path = '/home/user/flagged.csv'

    assert os.path.exists(truth_path), f"Ground truth file {truth_path} is missing."
    assert os.path.exists(preds_path), f"Predictions file {preds_path} is missing."

    truth = load_data(truth_path)
    preds = load_data(preds_path)

    if not truth and not preds:
        pytest.fail("Both truth and predictions are empty. F1=0.0")

    matched_preds = set()
    matched_truth = set()

    # Greedy matching with +/- 1 second tolerance
    for p in preds:
        p_user, p_time = p

        # Find all truth candidates that match the user_id and are within +/- 1 second
        candidates = [
            t for t in truth 
            if t[0] == p_user and abs(t[1] - p_time) <= 1 and t not in matched_truth
        ]

        if candidates:
            # Match with the closest time
            best_match = min(candidates, key=lambda t: abs(t[1] - p_time))
            matched_truth.add(best_match)
            matched_preds.add(p)

    tp = len(matched_preds)
    fp = len(preds) - tp
    fn = len(truth) - len(matched_truth)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    assert f1 >= 0.95, (
        f"F1 Score {f1:.4f} is below the 0.95 threshold. "
        f"(Precision: {precision:.4f}, Recall: {recall:.4f}, TP: {tp}, FP: {fp}, FN: {fn})"
    )