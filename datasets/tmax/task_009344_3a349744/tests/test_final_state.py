# test_final_state.py

import os
import json
import math
import pytest

def test_shared_library_exists():
    lib_path = "/home/user/network_sim/lib/libdiffusion.so"
    assert os.path.isfile(lib_path), f"Shared library not found at {lib_path}. Did you compile the C code?"

def test_analyze_script_exists():
    script_path = "/home/user/network_sim/analyze.py"
    assert os.path.isfile(script_path), f"Python script not found at {script_path}."

def test_summary_json_exists_and_format():
    summary_path = "/home/user/network_sim/results/summary.json"
    assert os.path.isfile(summary_path), f"Results file not found at {summary_path}."

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    assert "mean_diffusion_score" in data, "Key 'mean_diffusion_score' is missing from summary.json."
    assert "lrt_p_value" in data, "Key 'lrt_p_value' is missing from summary.json."

    assert isinstance(data["mean_diffusion_score"], (int, float)), "'mean_diffusion_score' must be a number."
    assert isinstance(data["lrt_p_value"], (int, float)), "'lrt_p_value' must be a number."

def test_summary_json_values():
    summary_path = "/home/user/network_sim/results/summary.json"
    if not os.path.isfile(summary_path):
        pytest.skip("summary.json not found.")

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("summary.json is not valid JSON.")

    # Expected values derived from the deterministic setup script (seed 42)
    expected_mean_score = 100.106516
    expected_p_value = 0.027003

    actual_mean = data.get("mean_diffusion_score")
    actual_p_value = data.get("lrt_p_value")

    if actual_mean is not None:
        assert math.isclose(actual_mean, expected_mean_score, abs_tol=1e-4), \
            f"mean_diffusion_score {actual_mean} does not match expected value {expected_mean_score} (within 1e-4 tolerance)."

    if actual_p_value is not None:
        assert math.isclose(actual_p_value, expected_p_value, abs_tol=1e-4), \
            f"lrt_p_value {actual_p_value} does not match expected value {expected_p_value} (within 1e-4 tolerance)."