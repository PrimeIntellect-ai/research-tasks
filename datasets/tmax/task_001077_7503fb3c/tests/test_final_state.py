# test_final_state.py

import json
import os
import pytest

def test_recovery_report_accuracy():
    """
    Evaluates the accuracy of the agent's recovery report against the ground truth.
    The metric is the ratio of exactly matching archive keys (with sorted list equality)
    to the total number of expected valid archives.
    The required accuracy threshold is >= 0.95.
    """
    expected_path = '/truth/expected_report.json'
    actual_path = '/app/recovery_report.json'

    assert os.path.isfile(expected_path), f"Ground truth report missing at {expected_path}"
    assert os.path.isfile(actual_path), f"Agent's recovery report missing at {actual_path}"

    try:
        with open(expected_path, 'r') as f:
            expected = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read expected report JSON: {e}")

    try:
        with open(actual_path, 'r') as f:
            actual = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read agent's recovery report JSON: {e}")

    total_keys = len(expected)
    assert total_keys > 0, "Expected report contains no keys, cannot calculate accuracy."

    correct_keys = 0
    for key, expected_list in expected.items():
        if key in actual:
            if sorted(actual[key]) == sorted(expected_list):
                correct_keys += 1

    accuracy = correct_keys / total_keys

    assert accuracy >= 0.95, (
        f"Accuracy metric failed: {accuracy:.4f} is below the 0.95 threshold. "
        f"Exactly matched {correct_keys} out of {total_keys} valid archives."
    )