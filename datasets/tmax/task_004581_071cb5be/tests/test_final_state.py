# test_final_state.py

import os
import json
import math

def test_analyze_script_exists_and_uses_mpi():
    script_path = "/home/user/analyze.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "mpi4py" in content or "MPI" in content, "The script does not seem to use mpi4py."

def test_mode1_plot_exists():
    plot_path = "/home/user/mode1.png"
    assert os.path.isfile(plot_path), f"Plot image {plot_path} does not exist."
    assert os.path.getsize(plot_path) > 0, f"Plot image {plot_path} is empty."

def test_results_json_structure_and_types():
    json_path = "/home/user/results.json"
    assert os.path.isfile(json_path), f"Results JSON {json_path} does not exist."

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not a valid JSON file."

    expected_keys = {
        "top_3_singular_values",
        "shapiro_p_value",
        "mean_peak_frequency"
    }

    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"

    # Check types
    assert isinstance(results["top_3_singular_values"], list), "top_3_singular_values must be a list."
    assert len(results["top_3_singular_values"]) == 3, "top_3_singular_values must contain exactly 3 elements."
    for val in results["top_3_singular_values"]:
        assert isinstance(val, (int, float)), "Elements of top_3_singular_values must be numbers."

    assert isinstance(results["shapiro_p_value"], (int, float)), "shapiro_p_value must be a number."
    assert isinstance(results["mean_peak_frequency"], (int, float)), "mean_peak_frequency must be a number."

    # Basic sanity checks on values
    assert results["shapiro_p_value"] >= 0.0 and results["shapiro_p_value"] <= 1.0, "p-value must be between 0 and 1."
    assert results["mean_peak_frequency"] > 0, "mean_peak_frequency should be positive."
    assert results["top_3_singular_values"][0] >= results["top_3_singular_values"][1] >= results["top_3_singular_values"][2], "Singular values should be sorted in descending order."