# test_final_state.py

import os
import json
import pytest

WORKSPACE_DIR = "/home/user/workspace"
NETWORK_ODE_FILE = os.path.join(WORKSPACE_DIR, "network_ode.py")
FIT_AND_COMPARE_FILE = os.path.join(WORKSPACE_DIR, "fit_and_compare.py")
FINAL_OUTPUT_FILE = os.path.join(WORKSPACE_DIR, "final_output.json")

def test_network_ode_fixed():
    assert os.path.isfile(NETWORK_ODE_FILE), f"{NETWORK_ODE_FILE} is missing."
    with open(NETWORK_ODE_FILE, 'r') as f:
        content = f.read()
    # The buggy code used `set(neighbors)` directly in the loop.
    # The fixed code should either not use `set` or use `sorted(set(...))` or similar.
    # We'll check that `for n in set(neighbors):` is no longer present.
    assert "for n in set(neighbors):" not in content, "The bug in network_ode.py (iterating over an unordered set) is still present."

def test_fit_and_compare_script_exists():
    assert os.path.isfile(FIT_AND_COMPARE_FILE), f"{FIT_AND_COMPARE_FILE} was not created."

def test_final_output_json():
    assert os.path.isfile(FINAL_OUTPUT_FILE), f"{FINAL_OUTPUT_FILE} was not generated."

    with open(FINAL_OUTPUT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{FINAL_OUTPUT_FILE} is not valid JSON.")

    assert "is_deterministic" in data, "Key 'is_deterministic' missing in final_output.json"
    assert data["is_deterministic"] is True, "Expected 'is_deterministic' to be true."

    assert "l2_error" in data, "Key 'l2_error' missing in final_output.json"
    assert isinstance(data["l2_error"], float), "Expected 'l2_error' to be a float."
    assert data["l2_error"] >= 0.0, "L2 error cannot be negative."