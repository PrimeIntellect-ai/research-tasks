# test_final_state.py

import os
import json
import pytest

def test_results_json_exists():
    """Verify that the results.json file has been created."""
    assert os.path.exists("/home/user/results.json"), "/home/user/results.json is missing. The task requires outputting results to this file."
    assert os.path.isfile("/home/user/results.json"), "/home/user/results.json exists but is not a file."

def test_results_json_content():
    """Verify the structure and correctness of the results.json file."""
    assert os.path.exists("/home/user/results.json"), "Cannot check content because /home/user/results.json is missing."
    assert os.path.exists("/home/user/ground_truth.json"), "Ground truth file is missing."

    with open("/home/user/results.json", "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/results.json is not a valid JSON file.")

    with open("/home/user/ground_truth.json", "r") as f:
        truth = json.load(f)

    # Validate valid_samples
    assert "valid_samples" in results, "Missing 'valid_samples' key in results.json."
    assert isinstance(results["valid_samples"], int), "'valid_samples' must be an integer."
    assert results["valid_samples"] == truth["valid_samples"], f"Incorrect 'valid_samples'. Expected {truth['valid_samples']}, got {results['valid_samples']}."

    # Validate sum_output_dim0
    assert "sum_output_dim0" in results, "Missing 'sum_output_dim0' key in results.json."
    assert isinstance(results["sum_output_dim0"], (int, float)), "'sum_output_dim0' must be a float."
    assert results["sum_output_dim0"] == truth["sum_output_dim0"], f"Incorrect 'sum_output_dim0'. Expected {truth['sum_output_dim0']}, got {results['sum_output_dim0']}."

    # Validate forward_pass_ms
    assert "forward_pass_ms" in results, "Missing 'forward_pass_ms' key in results.json."
    assert isinstance(results["forward_pass_ms"], (int, float)), "'forward_pass_ms' must be a float."
    assert results["forward_pass_ms"] > 0, f"'forward_pass_ms' must be a positive number, got {results['forward_pass_ms']}."