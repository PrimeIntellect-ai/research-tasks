# test_final_state.py

import os
import math
import pytest

def test_final_phases_exists():
    """Verify that final_phases.csv exists."""
    assert os.path.isfile("/home/user/final_phases.csv"), "/home/user/final_phases.csv was not generated."

def test_final_phases_content():
    """Verify the content of final_phases.csv matches the expected values."""
    csv_path = "/home/user/final_phases.csv"

    if not os.path.isfile(csv_path):
        pytest.fail(f"File {csv_path} is missing.")

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 6, f"Expected 6 lines in {csv_path}, got {len(lines)}."

    expected_values = {
        0: 2.222383,
        1: 2.302061,
        2: 2.302061,
        3: 2.441113,
        4: 2.441113,
        5: 2.463385
    }

    for line in lines:
        parts = line.split(",")
        assert len(parts) == 2, f"Invalid line format in {csv_path}: '{line}'"

        try:
            node_id = int(parts[0])
            phase = float(parts[1])
        except ValueError:
            pytest.fail(f"Could not parse node_id or phase as numbers in line: '{line}'")

        assert not math.isnan(phase), f"Phase for node {node_id} is NaN."
        assert not math.isinf(phase), f"Phase for node {node_id} is Inf."

        assert node_id in expected_values, f"Unexpected node_id {node_id} in output."

        expected_phase = expected_values[node_id]
        assert abs(phase - expected_phase) < 0.01, f"Phase for node {node_id} is {phase}, expected approx {expected_phase}."