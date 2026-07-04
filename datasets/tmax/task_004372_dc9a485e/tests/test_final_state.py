# test_final_state.py

import os
import json
import pytest

def test_convergence_results_exists_and_valid():
    results_path = "/home/user/convergence_results.json"

    assert os.path.isfile(results_path), f"The expected output file {results_path} does not exist. Did you run the controller?"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {results_path} does not contain valid JSON.")

    assert "status" in data, "The 'status' field is missing from the JSON output."
    assert data["status"] == "converged", f"Expected status 'converged', but got '{data['status']}'."

    assert "history" in data, "The 'history' field is missing from the JSON output."
    assert isinstance(data["history"], list), "The 'history' field should be a list."
    assert len(data["history"]) == 15, f"Expected 15 elements in the history array, but got {len(data['history'])}."

def test_sim_backend_executable_exists():
    executable_path = "/home/user/sim_backend"
    assert os.path.isfile(executable_path), f"The compiled executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."