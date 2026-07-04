# test_final_state.py

import os
import pytest

def load_set(path):
    try:
        with open(path, 'r') as f:
            return set([line.strip() for line in f.readlines() if line.strip()])
    except FileNotFoundError:
        return set()

def test_result_f1_score():
    """Test that the generated result.csv achieves an F1 score >= 0.95 against the truth."""
    truth_path = '/app/.hidden/true_paths.csv'
    pred_path = '/home/user/result.csv'

    assert os.path.isfile(truth_path), f"Truth file missing: {truth_path}"
    assert os.path.isfile(pred_path), f"Output file missing: {pred_path}. Did your script run and generate it?"

    truth = load_set(truth_path)
    pred = load_set(pred_path)

    if not truth and not pred:
        f1 = 1.0
    else:
        tp = len(truth.intersection(pred))
        fp = len(pred - truth)
        fn = len(truth - pred)

        if tp == 0:
            f1 = 0.0
        else:
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 Score {f1:.4f} is below the 0.95 threshold. TP: {len(truth.intersection(pred))}, FP: {len(pred - truth)}, FN: {len(truth - pred)}"

def test_script_exists():
    """Test that the bash script was created at the expected location."""
    script_path = '/home/user/graph_query.sh'
    assert os.path.isfile(script_path), f"Script missing: {script_path}"