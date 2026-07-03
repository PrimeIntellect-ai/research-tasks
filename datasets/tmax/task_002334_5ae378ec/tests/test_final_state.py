# test_final_state.py
import json
import os
import pytest

def compute_f1(pred, truth):
    pred_set = set(pred)
    truth_set = set(truth)
    if not pred_set and not truth_set: 
        return 1.0
    if not pred_set or not truth_set: 
        return 0.0

    tp = len(pred_set & truth_set)
    fp = len(pred_set - truth_set)
    fn = len(truth_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    if precision + recall == 0: 
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def test_threat_report_f1_score():
    report_path = '/home/user/threat_report.json'
    assert os.path.isfile(report_path), f"Threat report file is missing at {report_path}"

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    truth_ips = ["10.0.0.5", "192.168.50.2", "2001:db8::ff00:42:8329"]
    truth_keys = [
        "SHA256:p2QAMXGrxoQzK+wM6fK+f9c/8M1e3k6H/9l2A1C3E4Q", 
        "MD5:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd:ee:ff:00"
    ]

    pred_ips = report.get("malicious_ips", [])
    pred_keys = report.get("weak_keys", [])

    f1_ips = compute_f1(pred_ips, truth_ips)
    f1_keys = compute_f1(pred_keys, truth_keys)
    overall_f1 = (f1_ips + f1_keys) / 2

    assert overall_f1 >= 0.95, (
        f"Overall F1 score is {overall_f1:.4f}, which is below the threshold of 0.95. "
        f"(IP F1: {f1_ips:.4f}, Key F1: {f1_keys:.4f})"
    )