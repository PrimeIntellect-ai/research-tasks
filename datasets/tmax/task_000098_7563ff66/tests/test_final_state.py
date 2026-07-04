# test_final_state.py

import os
import re
import pytest

def test_nginx_fixed_conf():
    path = "/home/user/nginx_fixed.conf"
    assert os.path.isfile(path), f"Expected {path} to exist."
    with open(path, "r") as f:
        content = f.read()
    assert "unix:/home/user/run/backend.sock" in content, "The fixed Nginx config does not contain the correct backend socket path."

def test_harden_script_exists():
    path = "/home/user/harden.sh"
    assert os.path.isfile(path), f"Expected {path} to exist."

def test_firewall_script_f1_score():
    path = "/home/user/firewall.sh"
    assert os.path.isfile(path), f"Expected {path} to exist. Ensure your harden.sh script generates it."

    with open(path, 'r') as f:
        content = f.read()

    extracted_ips = set(re.findall(r'ufw deny from ([0-9\.]+)', content))
    ground_truth = {'192.168.1.100', '10.0.0.55'}

    tp = len(extracted_ips.intersection(ground_truth))
    fp = len(extracted_ips - ground_truth)
    fn = len(ground_truth - extracted_ips)

    if tp == 0:
        f1 = 0.0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 score of identified IPs is {f1:.2f}, expected >= 0.95. Extracted IPs: {extracted_ips}"

def test_firewall_script_executable():
    path = "/home/user/firewall.sh"
    if not os.path.isfile(path):
        pytest.skip("firewall.sh does not exist, skipping executable check.")
    assert os.access(path, os.X_OK), f"Expected {path} to be executable."