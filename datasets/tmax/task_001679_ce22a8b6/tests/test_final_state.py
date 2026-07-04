# test_final_state.py

import os
import json
import pytest

def get_pairs(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    pairs = set()
    for item in data:
        sanctioned_id = item.get("sanctioned_id")
        hub_id = item.get("hub_id")
        if sanctioned_id is not None and hub_id is not None:
            pairs.add((sanctioned_id, hub_id))
    return pairs

def test_compliance_report_f1_score():
    report_path = "/home/user/compliance_report.json"
    golden_path = "/app/golden_report.json"

    assert os.path.isfile(report_path), f"Output file {report_path} does not exist."
    assert os.path.isfile(golden_path), f"Golden file {golden_path} does not exist."

    agent_pairs = get_pairs(report_path)
    golden_pairs = get_pairs(golden_path)

    true_positives = len(agent_pairs.intersection(golden_pairs))
    false_positives = len(agent_pairs - golden_pairs)
    false_negatives = len(golden_pairs - agent_pairs)

    if true_positives == 0:
        precision = 0.0
        recall = 0.0
        f1_score = 0.0
    else:
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1_score = 2 * (precision * recall) / (precision + recall)

    assert f1_score >= 0.99, f"F1 Score is {f1_score:.4f}, which is below the threshold of 0.99. Precision: {precision:.4f}, Recall: {recall:.4f}."