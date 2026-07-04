# test_final_state.py

import os
import json
import math
import pytest

def test_analysis_output_exists():
    filepath = "/home/user/analysis_output.json"
    assert os.path.exists(filepath), f"Missing expected output file: {filepath}"
    assert os.path.isfile(filepath), f"Expected a file, but found a directory: {filepath}"

def test_analysis_output_content():
    filepath = "/home/user/analysis_output.json"
    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON from {filepath}: {e}")

    expected_keys = {"most_similar_profiles", "profile_distance", "spatial_distance"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected. Found: {list(data.keys())}"

    profiles = data["most_similar_profiles"]
    assert isinstance(profiles, list), "most_similar_profiles must be a list"
    assert sorted(profiles) == ["S1", "S2"], f"Expected most_similar_profiles to be ['S1', 'S2'], got {profiles}"

    profile_distance = data["profile_distance"]
    assert isinstance(profile_distance, (int, float)), "profile_distance must be a number"
    assert math.isclose(profile_distance, 0.7788, abs_tol=1e-4), f"Expected profile_distance to be ~0.7788, got {profile_distance}"

    spatial_distance = data["spatial_distance"]
    assert isinstance(spatial_distance, (int, float)), "spatial_distance must be a number"
    assert math.isclose(spatial_distance, 5.0000, abs_tol=1e-4), f"Expected spatial_distance to be ~5.0000, got {spatial_distance}"