# test_final_state.py
import os
import json
import math

def test_results_file_exists():
    """Test that the final results JSON file exists."""
    results_path = "/home/user/spectroscopy_results.json"
    assert os.path.isfile(results_path), f"Missing required file: {results_path}"

def test_results_content():
    """Test the contents of the results JSON file."""
    results_path = "/home/user/spectroscopy_results.json"
    assert os.path.isfile(results_path), f"Missing required file: {results_path}"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_path} is not valid JSON."

    # Check required keys
    expected_keys = {"bic_1peak", "bic_2peak", "best_model", "bootstrap_ci_x1", "bootstrap_ci_x2"}
    for key in expected_keys:
        assert key in results, f"Missing key '{key}' in {results_path}"

    # Check best model
    assert results["best_model"] == "2-peak", f"Expected best_model to be '2-peak', got '{results['best_model']}'"

    # Check BIC values
    assert isinstance(results["bic_1peak"], (int, float)), "bic_1peak must be a number"
    assert isinstance(results["bic_2peak"], (int, float)), "bic_2peak must be a number"
    assert results["bic_2peak"] < results["bic_1peak"], "Expected bic_2peak to be less than bic_1peak"

    # We compute the exact expected values derived from the data
    # (In a real test, we might re-run the exact computation, but here we can check the approximate bounds 
    # based on the golden script logic and typical output for this specific dataset).
    # Since we don't have numpy/pandas/scipy in stdlib, we will check if the values are within the expected ranges 
    # based on the fixed seed generation in setup_data.py and the golden script.

    # Expected approximate values from golden script (with seed 101 for data, 42 for bootstrap):
    # bic_1peak: ~ 447.88
    # bic_2peak: ~ 231.81
    # bootstrap_ci_x1: ~ [41.38, 42.66]
    # bootstrap_ci_x2: ~ [57.17, 58.74]

    # We will just verify the structure and approximate values to ensure the task was completed correctly.
    assert math.isclose(results["bic_1peak"], 447.88, abs_tol=5.0), f"bic_1peak {results['bic_1peak']} is too far from expected."
    assert math.isclose(results["bic_2peak"], 231.81, abs_tol=5.0), f"bic_2peak {results['bic_2peak']} is too far from expected."

    ci_x1 = results["bootstrap_ci_x1"]
    assert isinstance(ci_x1, list) and len(ci_x1) == 2, "bootstrap_ci_x1 must be a list of 2 numbers"
    assert math.isclose(ci_x1[0], 41.38, abs_tol=1.0), f"bootstrap_ci_x1 lower bound {ci_x1[0]} is too far from expected."
    assert math.isclose(ci_x1[1], 42.66, abs_tol=1.0), f"bootstrap_ci_x1 upper bound {ci_x1[1]} is too far from expected."
    assert ci_x1[0] < ci_x1[1], "bootstrap_ci_x1 lower bound must be less than upper bound"

    ci_x2 = results["bootstrap_ci_x2"]
    assert isinstance(ci_x2, list) and len(ci_x2) == 2, "bootstrap_ci_x2 must be a list of 2 numbers"
    assert math.isclose(ci_x2[0], 57.17, abs_tol=1.0), f"bootstrap_ci_x2 lower bound {ci_x2[0]} is too far from expected."
    assert math.isclose(ci_x2[1], 58.74, abs_tol=1.0), f"bootstrap_ci_x2 upper bound {ci_x2[1]} is too far from expected."
    assert ci_x2[0] < ci_x2[1], "bootstrap_ci_x2 lower bound must be less than upper bound"