# test_final_state.py

import os
import re
import pytest

def compute_f1(pred_file, true_ips):
    try:
        with open(pred_file, "r") as f:
            content = f.read()
    except Exception:
        return 0.0

    pred_ips = set(re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", content))
    true_set = set(true_ips)

    tp = len(pred_ips.intersection(true_set))
    fp = len(pred_ips - true_set)
    fn = len(true_set - pred_ips)

    if tp == 0:
        return 0.0

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1

def test_extracted_ips_f1_score():
    pred_file = "/home/user/extracted_ips.txt"
    assert os.path.exists(pred_file), f"File {pred_file} does not exist."

    true_ips = ["10.5.12.4", "192.168.100.52", "172.16.8.88"]
    f1 = compute_f1(pred_file, true_ips)

    assert f1 >= 0.8, f"F1 score for extracted IPs is {f1:.2f}, which is below the threshold of 0.8."

def test_generate_fw_script_exists():
    script_path = "/home/user/generate_fw.py"
    assert os.path.exists(script_path), f"Python script {script_path} does not exist."

def test_apply_firewall_script_exists_and_contains_iptables():
    script_path = "/home/user/apply_firewall.sh"
    assert os.path.exists(script_path), f"Bash script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "iptables" in content, f"Bash script {script_path} does not contain 'iptables' commands."