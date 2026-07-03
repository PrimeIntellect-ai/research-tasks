# test_final_state.py

import os
import pytest

def test_malicious_ips_f1_score():
    pred_path = "/home/user/malicious_ips.txt"
    truth_path = "/opt/verifier/ground_truth_ips.txt"

    assert os.path.isfile(pred_path), f"Output file {pred_path} is missing. Did you generate the malicious IPs list?"
    assert os.path.isfile(truth_path), f"Ground truth file {truth_path} is missing."

    with open(pred_path, "r") as f:
        preds = set(line.strip() for line in f if line.strip())

    with open(truth_path, "r") as f:
        truths = set(line.strip() for line in f if line.strip())

    tp = len(preds & truths)
    fp = len(preds - truths)
    fn = len(truths - preds)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    assert f1 >= 0.95, f"F1-score {f1:.4f} is below threshold 0.95 (TP={tp}, FP={fp}, FN={fn}). Improve your log analyzer's detection logic."

def test_patched_server_exists_and_executable():
    server_path = "/home/user/patched_httpd"
    assert os.path.isfile(server_path), f"Patched server binary {server_path} is missing. Did you compile and save it to the correct location?"
    assert os.access(server_path, os.X_OK), f"Patched server binary {server_path} is not executable."

def test_log_analyzer_exists_and_executable():
    analyzer_path = "/home/user/log_analyzer"
    assert os.path.isfile(analyzer_path), f"Log analyzer binary {analyzer_path} is missing. Did you compile your C program?"
    assert os.access(analyzer_path, os.X_OK), f"Log analyzer binary {analyzer_path} is not executable."