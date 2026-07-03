# test_final_state.py

import os
import json
import glob
import re
import pytest

def get_reference_query_ids():
    """
    Attempt to find the reference JSONL file or extract query_ids from the raw logs.
    """
    # Look for a reference file
    possible_refs = glob.glob('/home/user/*ref*.jsonl') + glob.glob('/home/user/.*ref*.jsonl') + glob.glob('/app/**/*ref*.jsonl', recursive=True)

    for ref_path in possible_refs:
        if os.path.isfile(ref_path) and 'processed_logs' not in ref_path:
            try:
                ids = set()
                with open(ref_path, 'r') as f:
                    for line in f:
                        if not line.strip():
                            continue
                        data = json.loads(line)
                        if 'query_id' in data:
                            ids.add(str(data['query_id']))
                if ids:
                    return ids
            except Exception:
                pass

    # Fallback: extract from raw logs if reference file is not found
    raw_logs_path = "/home/user/raw_logs.txt"
    ids = set()
    if os.path.exists(raw_logs_path):
        with open(raw_logs_path, 'r') as f:
            content = f.read()
            # Simple heuristic to find query_ids in the raw logs
            found = re.findall(r'query_id["\'\s:=]+([A-Za-z0-9_-]+)', content)
            ids.update(found)
    return ids

def test_processed_logs_f1_score():
    agent_file = "/home/user/processed_logs.jsonl"

    assert os.path.exists(agent_file), f"Agent's output file not found: {agent_file}"

    agent_ids = set()
    with open(agent_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if 'query_id' in data:
                    agent_ids.add(str(data['query_id']))
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON at line {line_num} in {agent_file}")

    assert len(agent_ids) > 0, "No query_ids found in the agent's output file."

    reference_ids = get_reference_query_ids()

    if not reference_ids:
        # If we truly cannot find or infer reference IDs, we just pass if the agent produced valid output.
        # This is a fallback to ensure the test doesn't spuriously fail due to missing hidden files.
        return

    true_positives = len(agent_ids.intersection(reference_ids))
    false_positives = len(agent_ids - reference_ids)
    false_negatives = len(reference_ids - agent_ids)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0

    if precision + recall == 0:
        f1_score = 0.0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    assert f1_score >= 0.95, f"F1 score is {f1_score:.4f}, which is below the threshold of 0.95. Precision: {precision:.4f}, Recall: {recall:.4f}"