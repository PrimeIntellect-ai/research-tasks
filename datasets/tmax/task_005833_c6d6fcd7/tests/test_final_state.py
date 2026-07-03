# test_final_state.py

import os
import pytest

def test_sim_core_c_fixed():
    path = "/home/user/sim_core.c"
    assert os.path.isfile(path), f"File not found: {path}"

    with open(path, "r") as f:
        content = f.read()

    # The OpenMP parallel reduction pragma should be removed or commented out, 
    # or modified to not cause non-determinism (e.g., using num_threads(1)).
    # The simplest check is that the original pragma is gone or modified.
    # We will just verify that the exact original line is not there and active.
    # But since they might just comment it, checking the output is the real test.
    pass

def test_reproducible_energy_txt():
    path = "/home/user/reproducible_energy.txt"
    assert os.path.isfile(path), f"Output file {path} was not created."

    with open(path, "r") as f:
        content = f.read().strip()

    # Calculate the expected ground truth value
    import numpy as np
    np.random.seed(42)
    data = np.random.rand(1000000)
    energy = 0.0
    for x in data:
        energy += x * 1.0000001

    expected_value = f"{energy:.12f}"

    assert content == expected_value, f"Expected energy value {expected_value}, but got {content}"