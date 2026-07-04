# test_final_state.py
import re
import os
import pytest

def test_alerts_log_f1_score_and_permissions():
    log_path = '/home/user/alerts.log'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Ensure your script runs and creates it."

    # Check permissions
    stat = os.stat(log_path)
    perms = oct(stat.st_mode)[-3:]
    assert perms == '600', f"Permissions of {log_path} are {perms}, expected 600."

    # Check F1 Score
    truth_frames = {45, 120, 315, 800, 1024, 1500, 1750}

    with open(log_path, 'r') as f:
        content = f.read()

    pred_frames = set(int(x) for x in re.findall(r'ALERT:\s*Frame\s*(\d+)', content))

    true_positives = len(truth_frames.intersection(pred_frames))
    false_positives = len(pred_frames - truth_frames)
    false_negatives = len(truth_frames - pred_frames)

    if true_positives == 0:
        f1_score = 0.0
    else:
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1_score = 2 * (precision * recall) / (precision + recall)

    assert f1_score >= 0.95, f"F1 Score is {f1_score:.4f}, expected >= 0.95. Truth frames: {truth_frames}, Predicted frames: {pred_frames}"