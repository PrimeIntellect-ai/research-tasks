# test_final_state.py
import json
import os
import pytest

def test_required_files_exist():
    """Check that the agent created the required Python files."""
    workspace = "/home/user/workspace"
    expected_files = ["ecc.py", "integration.py", "test_ecc.py", "results.json"]

    for f in expected_files:
        path = os.path.join(workspace, f)
        assert os.path.isfile(path), f"Required file {path} is missing."

def test_results_json_metric():
    """
    Evaluate the metric threshold based on the agent's generated results.json.
    The agent must have processed at least 500 payloads with an Error Recovery Rate >= 0.95.
    """
    results_path = "/home/user/workspace/results.json"
    assert os.path.isfile(results_path), f"{results_path} is missing."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse {results_path} as valid JSON.")

    assert isinstance(results, list), "results.json must contain a JSON array."
    assert len(results) >= 500, f"Expected at least 500 results in results.json, got {len(results)}."

    success_count = sum(1 for item in results if item.get("status") == "success")
    total_count = len(results)

    recovery_rate = success_count / total_count

    assert recovery_rate >= 0.95, (
        f"Error Recovery Rate metric failed. "
        f"Threshold: >= 0.95, Actual: {recovery_rate:.4f} "
        f"({success_count}/{total_count} successful verifications)."
    )