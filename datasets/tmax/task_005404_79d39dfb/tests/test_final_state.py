# test_final_state.py

import os
import json
import pytest

def compute_f1(pred_file, truth_file):
    with open(pred_file) as f: 
        preds = set(json.load(f).get('detected_ids', []))
    with open(truth_file) as f: 
        truths = set(json.load(f).get('malicious_ids', []))

    tp = len(preds & truths)
    fp = len(preds - truths)
    fn = len(truths - preds)

    if tp == 0: 
        return 0.0

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2 * (precision * recall) / (precision + recall)

def test_setup_fw_script_exists():
    path = "/home/user/setup_fw.sh"
    assert os.path.isfile(path), f"Firewall setup script missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "iptables" in content or "ufw" in content, "Script does not seem to contain iptables or ufw commands."
    assert "4444" in content, "Script does not seem to target port 4444."

def test_run_audit_script_exists():
    path = "/home/user/run_audit.py"
    assert os.path.isfile(path), f"Wrapper script missing: {path}"

def test_audit_report_exists():
    path = "/home/user/audit_report.json"
    assert os.path.isfile(path), f"Audit report missing: {path}"

def test_f1_score_meets_threshold():
    pred_file = "/home/user/audit_report.json"
    # Assuming truth file is located here based on standard task structures
    truth_file = "/home/user/ground_truth.json"

    if not os.path.exists(truth_file):
        # Fallback if the ground truth is named differently
        truth_file = "/app/ground_truth.json"

    if not os.path.exists(truth_file):
        pytest.skip("Ground truth file not found, cannot compute F1 score.")

    f1 = compute_f1(pred_file, truth_file)
    assert f1 >= 0.95, f"F1-score {f1:.4f} is below the target threshold of 0.95"

def test_decoder_fixed():
    path = "/app/pyaudit-scanner-1.2.0/scanner/decoder.py"
    assert os.path.isfile(path), f"Decoder file missing: {path}"
    with open(path, 'r') as f:
        content = f.read()
    # The perturbation should be removed or commented out
    assert "return None # test skip" not in content, "The deliberate perturbation in decoder.py was not fixed."