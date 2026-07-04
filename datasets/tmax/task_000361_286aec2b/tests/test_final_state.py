# test_final_state.py
import json
import os
import pytest

def load_logs(filepath):
    logs = set()
    with open(filepath, 'r') as f:
        for line in f:
            if not line.strip(): 
                continue
            d = json.loads(line)
            # Freeze dict to make it hashable
            logs.add(frozenset(d.items()))
    return logs

def test_jaccard_similarity():
    golden_path = '/opt/golden_processed_logs.jsonl'
    actual_path = '/home/user/processed_logs.jsonl'

    assert os.path.exists(golden_path), f"Golden file {golden_path} is missing."
    assert os.path.exists(actual_path), f"Actual output file {actual_path} is missing. The ETL worker may not have run successfully or wrote to the wrong path."

    target = load_logs(golden_path)
    actual = load_logs(actual_path)

    intersection = len(target.intersection(actual))
    union = len(target.union(actual))
    jaccard = intersection / union if union > 0 else 0

    assert jaccard >= 0.99, f"Jaccard similarity {jaccard:.4f} is below threshold 0.99. Target logs: {len(target)}, Actual logs: {len(actual)}, Intersection: {intersection}."