# test_final_state.py

import os
import ast
import pytest

def test_summary_file_exists_and_correct():
    """Test that the summary.txt file was generated and contains the correct log counts."""
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"The file {summary_path} was not generated. Did you run the script successfully?"

    with open(summary_path, "r") as f:
        content = f.read().strip()

    try:
        results = ast.literal_eval(content)
    except Exception as e:
        pytest.fail(f"Failed to parse the contents of {summary_path}. Expected a dictionary string. Error: {e}")

    expected_results = {'ERROR': 2, 'CRITICAL': 1}
    assert results == expected_results, f"The summary results are incorrect. Expected {expected_results}, got {results}."

def test_json_conflict_resolved():
    """Test that the conflicting local json.py module has been removed or renamed."""
    json_path = "/home/user/json.py"
    assert not os.path.isfile(json_path), f"The conflicting module {json_path} still exists. It must be removed or renamed to resolve the dependency conflict."

def test_log_aggregator_fixed():
    """Test that log_aggregator.py has been modified to properly decode the base64 config."""
    script_path = "/home/user/log_aggregator.py"
    assert os.path.isfile(script_path), f"Missing {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    assert "b64decode" in content, "The log_aggregator.py script does not appear to use base64 decoding for the config data."