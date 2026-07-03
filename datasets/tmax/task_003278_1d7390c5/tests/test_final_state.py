# test_final_state.py

import os
import pytest

def test_recovery_distance_file():
    """Verify that the recovery distance file exists and contains the correct calculated distance."""
    recovery_path = "/home/user/recovery_distance.txt"
    assert os.path.exists(recovery_path), f"File not found: {recovery_path}"

    with open(recovery_path, "r") as f:
        content = f.read().strip()

    expected_distance = "5570.22"
    assert content == expected_distance, f"Expected distance '{expected_distance}', but got '{content}' in {recovery_path}"

def test_mre_c_exists():
    """Verify that the minimal reproducible example C file was created."""
    mre_path = "/home/user/mre.c"
    assert os.path.exists(mre_path), f"MRE source file not found: {mre_path}"

def test_haversine_c_fixed():
    """Verify that the haversine.c file no longer contains the specific buggy line."""
    haversine_path = "/home/user/haversine.c"
    assert os.path.exists(haversine_path), f"File not found: {haversine_path}"

    with open(haversine_path, "r") as f:
        content = f.read()

    # The original buggy code was exactly "cos(lat1) * cos(lat2)"
    # We check that this exact string is gone, implying it was modified.
    assert "cos(lat1) * cos(lat2)" not in content, (
        f"The bug in {haversine_path} does not appear to be fixed. "
        "It still contains the buggy 'cos(lat1) * cos(lat2)' calculation."
    )