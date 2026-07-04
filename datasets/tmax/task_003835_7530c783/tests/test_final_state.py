# test_final_state.py
import os
import re
import pytest

def test_recovery_cypher_metric():
    expected_source = 8374
    expected_targets = {1020, 45, 9991}
    output_path = "/home/user/recovery.cypher"

    assert os.path.exists(output_path), f"Output file not found: {output_path}"

    with open(output_path, "r") as f:
        content = f.read()

    # Parse output, allowing for optional spaces after the colon
    pattern = r"CREATE \(n:Node \{id:\s*(\d+)\}\)-\[:CONNECTED_TO\]->\(m:Node \{id:\s*(\d+)\}\);"
    matches = re.findall(pattern, content)

    actual_targets = set()
    valid_source_count = 0

    for src, tgt in matches:
        if int(src) == expected_source:
            actual_targets.add(int(tgt))
            valid_source_count += 1

    assert valid_source_count > 0, f"No valid Cypher statements found for the expected source node ID ({expected_source}) in {output_path}."

    true_positives = len(actual_targets.intersection(expected_targets))
    false_positives = len(actual_targets - expected_targets)
    false_negatives = len(expected_targets - actual_targets)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0

    if precision + recall == 0:
        f1_score = 0.0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    assert f1_score >= 1.0, (
        f"F1 score {f1_score:.2f} is below the required threshold of 1.0.\n"
        f"Expected targets for node {expected_source}: {expected_targets}\n"
        f"Actual valid targets found: {actual_targets}"
    )