# test_final_state.py

import os
import json
import socket
import pytest

def test_results_json():
    """Verify that results.json exists and contains the correct typed results."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"The file {results_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {results_path} does not contain valid JSON.")

    expected = {
        "python": 40,
        "ruby": True,
        "node": 9
    }

    assert results == expected, f"Expected {expected}, but got {results}."

    # Ensure types are exactly as expected (e.g. not 1 for True)
    assert type(results["python"]) is int, "Python result should be an integer."
    assert type(results["ruby"]) is bool, "Ruby result should be a boolean."
    assert type(results["node"]) is int, "Node result should be an integer."

def test_run_tests_script_exists():
    """Verify that the run_tests.py script exists."""
    script_path = "/home/user/run_tests.py"
    assert os.path.isfile(script_path), f"The test script {script_path} does not exist."

def test_server_listening():
    """Verify that the server is running in the background and listening on port 8080."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "The server is not listening on port 8080."