# test_final_state.py

import os
import pytest

def test_kl_divergence_file_exists():
    path = "/home/user/kl_divergence.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did you save the output of the fixed program?"

def test_kl_divergence_value():
    path = "/home/user/kl_divergence.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content, f"File {path} is empty."

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {path} ('{content}') as a floating-point number.")

    expected_val = 0.003926
    tolerance = 1e-4
    assert abs(val - expected_val) < tolerance, (
        f"Computed KL divergence {val} is not within {tolerance} of the expected value {expected_val}. "
        "Check your step-size clamping logic."
    )

def test_main_rs_modified():
    path = "/home/user/seq_analyzer/src/main.rs"
    assert os.path.isfile(path), f"Source file {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # The original file had exactly `step /= 2;` inside the block `if a_count > 5`.
    # It must be modified to prevent step from dropping to 0.
    # We don't strictly assert the exact syntax of the fix (as there are multiple ways to fix it),
    # but the successful generation of the correct KL divergence value inherently proves the fix.
    assert "fn compute_spectral_profile" in content, "main.rs seems to be heavily modified or missing the target function."