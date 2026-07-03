# test_final_state.py

import os
import json
import pytest

def solve_vdp(y1, y2, t_end, tol):
    """
    Python implementation of the fixed Rust integrator to compute truth values.
    """
    t = 0.0
    dt = 0.01
    mu = 1.0

    while t < t_end:
        if t + dt > t_end:
            dt = t_end - t

        y1_e = y1 + dt * y2
        y2_e = y2 + dt * (mu * (1.0 - y1*y1) * y2 - y1)

        f2_start = mu * (1.0 - y1*y1) * y2 - y1
        f2_end = mu * (1.0 - y1_e*y1_e) * y2_e - y1_e

        y1_h = y1 + (dt / 2.0) * (y2 + (y2 + dt * f2_start))
        y2_h = y2 + (dt / 2.0) * (f2_start + f2_end)

        error = max(((y1_e - y1_h)**2 + (y2_e - y2_h)**2)**0.5, 1e-10)

        if error < tol:
            y1 = y1_h
            y2 = y2_h
            t += dt

        dt = dt * (tol / error)**0.5
        dt = max(1e-5, min(dt, 0.1))

    return y1, y2

def test_workflow_notebook_exists():
    """Verify that the Jupyter Notebook was created."""
    assert os.path.exists("/home/user/workflow.ipynb"), "/home/user/workflow.ipynb is missing"

def test_ml_training_json_exists_and_valid():
    """Verify that the ml_training.json file exists, is valid JSON, and has 100 entries."""
    json_path = "/home/user/ml_training.json"
    assert os.path.exists(json_path), f"{json_path} is missing"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON")

    assert isinstance(data, list), "JSON root must be a list"
    assert len(data) == 100, f"Expected 100 elements in the JSON array, got {len(data)}"

    # Check id=0
    item_0 = next((item for item in data if item.get("id") == 0), None)
    assert item_0 is not None, "Item with id=0 not found in the JSON array"

    expected_y1, expected_y2 = solve_vdp(1.0, 0.0, 10.0, 1e-4)

    assert "final_y1" in item_0, "Key 'final_y1' is missing in item 0"
    assert "final_y2" in item_0, "Key 'final_y2' is missing in item 0"

    # Allow a small floating point tolerance due to potential minor differences across languages/compilers
    assert abs(item_0["final_y1"] - expected_y1) < 1e-5, f"final_y1 mismatch for id=0: expected approx {expected_y1}, got {item_0['final_y1']}"
    assert abs(item_0["final_y2"] - expected_y2) < 1e-5, f"final_y2 mismatch for id=0: expected approx {expected_y2}, got {item_0['final_y2']}"

def test_raw_data_csv_exists():
    """Verify that the intermediate raw_data.csv file was generated."""
    assert os.path.exists("/home/user/raw_data.csv"), "/home/user/raw_data.csv is missing"