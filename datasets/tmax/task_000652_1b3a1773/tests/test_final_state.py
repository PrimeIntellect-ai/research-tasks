# test_final_state.py

import os
import json
import subprocess
import pytest

def test_run_test_sh_passes():
    """Verify that running the test script passes successfully."""
    script_path = "/home/user/run_test.sh"
    assert os.path.isfile(script_path), f"File not found: {script_path}"

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_test.sh failed with output: {result.stdout}\n{result.stderr}"
    assert "Build Passed." in result.stdout, "run_test.sh did not print 'Build Passed.'"

def test_results_json_content():
    """Verify that results.json has the correct 4 events."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"File not found: {results_path}"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    assert isinstance(results, list), "results.json should contain a JSON array"
    assert len(results) == 4, f"Expected exactly 4 events in results.json, found {len(results)}"

    # Check that the 4 specific events are present based on their messages
    expected_messages = {
        "User login",
        "Database timeout",
        "User logout",
        "High memory usage"
    }

    actual_messages = {item.get("message") for item in results}
    assert expected_messages.issubset(actual_messages), f"Missing expected events. Expected messages: {expected_messages}, Found: {actual_messages}"