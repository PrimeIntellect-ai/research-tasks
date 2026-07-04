# test_final_state.py
import os
import json
import math

def test_virtual_environment_exists():
    """Verify that the Python virtual environment was created."""
    venv_python = "/home/user/sim_env/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment python executable not found at {venv_python}. Did you create the virtual environment?"

def test_pcr_results_json():
    """Verify the contents of the pcr_results.json file."""
    results_file = "/home/user/pcr_results.json"
    assert os.path.isfile(results_file), f"Results file not found at {results_file}."

    with open(results_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_file} does not contain valid JSON."

    expected_keys = {
        "reference_amplified",
        "reference_total",
        "mutants_amplified",
        "mutants_total",
        "p_value"
    }

    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"Missing keys in JSON output: {missing_keys}"

    assert results["reference_amplified"] == 10, f"Expected reference_amplified to be 10, got {results['reference_amplified']}."
    assert results["reference_total"] == 100, f"Expected reference_total to be 100, got {results['reference_total']}."
    assert results["mutants_amplified"] == 60, f"Expected mutants_amplified to be 60, got {results['mutants_amplified']}."
    assert results["mutants_total"] == 100, f"Expected mutants_total to be 100, got {results['mutants_total']}."

    expected_p_value = 5.556284345244583e-13
    actual_p_value = results["p_value"]

    assert isinstance(actual_p_value, float), f"Expected p_value to be a float, got {type(actual_p_value)}."
    assert math.isclose(actual_p_value, expected_p_value, rel_tol=1e-5, abs_tol=1e-15), \
        f"Expected p_value to be close to {expected_p_value}, got {actual_p_value}."