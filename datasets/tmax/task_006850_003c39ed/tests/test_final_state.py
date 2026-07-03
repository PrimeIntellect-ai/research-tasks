# test_final_state.py

import os
import json
import pytest

def test_scripts_exist():
    """Verify that the required scripts exist and have correct permissions."""
    py_script = "/home/user/analyze_deadlocks.py"
    bash_script = "/home/user/run_analysis.sh"

    assert os.path.exists(py_script), f"{py_script} is missing."
    assert os.path.isfile(py_script), f"{py_script} is not a file."

    assert os.path.exists(bash_script), f"{bash_script} is missing."
    assert os.path.isfile(bash_script), f"{bash_script} is not a file."
    assert os.access(bash_script, os.X_OK), f"{bash_script} is not executable."

def test_json_report():
    """Verify the deadlock report matches the required structure and values."""
    report_path = "/home/user/deadlock_report.json"
    assert os.path.exists(report_path), f"{report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON.")

    # Check bottleneck_tx
    assert "bottleneck_tx" in data, "Key 'bottleneck_tx' is missing from the JSON report."
    assert data["bottleneck_tx"] == "T6", f"Expected bottleneck_tx to be 'T6', got '{data['bottleneck_tx']}'."

    # Check deadlocks
    assert "deadlocks" in data, "Key 'deadlocks' is missing from the JSON report."
    deadlocks = data["deadlocks"]
    assert isinstance(deadlocks, list), "'deadlocks' should be a list."
    assert len(deadlocks) == 2, f"Expected 2 deadlock cycles, found {len(deadlocks)}."

    cycle_sets = [set(cycle) for cycle in deadlocks]
    assert {"T1", "T2", "T3"} in cycle_sets, "Cycle involving T1, T2, T3 is missing from deadlocks."
    assert {"T4", "T5"} in cycle_sets, "Cycle involving T4, T5 is missing from deadlocks."

    # Check in_degree_centrality
    assert "in_degree_centrality" in data, "Key 'in_degree_centrality' is missing from the JSON report."
    centrality = data["in_degree_centrality"]
    assert isinstance(centrality, dict), "'in_degree_centrality' should be an object (dictionary)."

    expected_centrality = {
        "T1": 0.125, "T2": 0.125, "T3": 0.125,
        "T4": 0.125, "T5": 0.125,
        "T6": 0.375,
        "T7": 0.0, "T8": 0.0, "T9": 0.0
    }

    for node, expected_val in expected_centrality.items():
        assert node in centrality, f"Node '{node}' is missing from in_degree_centrality."
        actual_val = centrality[node]
        assert isinstance(actual_val, (int, float)), f"Centrality for '{node}' must be a number."
        assert abs(actual_val - expected_val) < 1e-6, f"Centrality for '{node}' expected to be {expected_val}, got {actual_val}."