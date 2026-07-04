# test_final_state.py

import os
import numpy as np
import pytest

def test_centroid_file_exists():
    path = "/home/user/centroid.txt"
    assert os.path.isfile(path), f"File missing: {path}"

def test_centroid_value():
    path = "/home/user/centroid.txt"
    with open(path, 'r') as f:
        content = f.read().strip()

    assert content, "Centroid file is empty."

    try:
        agent_vals = np.array([float(x.strip()) for x in content.split(',')])
    except ValueError:
        pytest.fail(f"Could not parse centroid values as floats. Found: {content}")

    assert agent_vals.shape == (2,), f"Expected exactly 2 values, got {agent_vals.shape[0]}."

    reference_vals = np.array([0.0, 0.0])
    distance = np.linalg.norm(agent_vals - reference_vals)

    threshold = 1e-5
    assert distance <= threshold, f"L2 distance {distance} exceeds threshold {threshold}. Agent centroid: {agent_vals}, Reference: {reference_vals}"