# test_final_state.py

import os
import pytest

def calculate_f1(true_positives, false_positives, false_negatives):
    if true_positives == 0:
        return 0.0
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    return 2 * (precision * recall) / (precision + recall)

def test_suspects_f1_score():
    suspects_path = '/home/user/suspects.txt'
    assert os.path.isfile(suspects_path), f"Output file missing at {suspects_path}"

    expected_data = {
        "192.168.1.55": ("1234", "../../../etc/passwd"),
        "10.0.0.4": ("9999", "uploads/..%2f..%2f/shadow"),
        "172.16.0.8": ("0000", "..\\..\\windows\\system32\\config\\sam")
    }

    with open(suspects_path, 'r') as f:
        lines = f.read().splitlines()

    parsed_agent_data = {}
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(',', 2)
        if len(parts) == 3:
            parsed_agent_data[parts[0]] = (parts[1], parts[2])

    expected_ips = set(expected_data.keys())
    agent_ips = set(parsed_agent_data.keys())

    tp = 0
    for ip in expected_ips.intersection(agent_ips):
        if parsed_agent_data[ip] == expected_data[ip]:
            tp += 1

    fp = len(agent_ips - expected_ips)
    fn = len(expected_ips) - tp

    f1 = calculate_f1(tp, fp, fn)

    assert f1 >= 0.95, f"F1 score {f1:.2f} is below the threshold of 0.95. TP: {tp}, FP: {fp}, FN: {fn}"

def test_base58_fixed():
    init_path = '/app/base58-2.1.1/__init__.py'
    base58_path = '/app/base58-2.1.1/base58.py'

    found_standard = False
    for path in [init_path, base58_path]:
        if os.path.isfile(path):
            with open(path, 'r') as f:
                content = f.read()
                if "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz" in content:
                    found_standard = True
                    break

    assert found_standard, "Standard BITCOIN_ALPHABET not found in the vendored base58 package. The package was not properly fixed."