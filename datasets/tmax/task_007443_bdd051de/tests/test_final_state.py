# test_final_state.py
import os
import re
import pytest

def test_results_file_exists():
    """Verify that the results file was created."""
    assert os.path.isfile("/home/user/results.txt"), "The file /home/user/results.txt does not exist."

def test_c_source_file_exists():
    """Verify that the C source file was created."""
    assert os.path.isfile("/home/user/fit_sampler.c"), "The file /home/user/fit_sampler.c does not exist."

def test_results_content():
    """Verify the contents of the results file."""
    results_path = "/home/user/results.txt"
    if not os.path.isfile(results_path):
        pytest.fail("results.txt not found.")

    with open(results_path, "r") as f:
        content = f.read()

    ols_match = re.search(r"OLS:\s*beta0=([^,]+),\s*beta1=([^,]+),\s*beta2=([^\s]+)", content)
    mcmc_match = re.search(r"MCMC:\s*beta0=([^,]+),\s*beta1=([^,]+),\s*beta2=([^\s]+)", content)

    assert ols_match is not None, "OLS line not found or formatted incorrectly in results.txt."
    assert mcmc_match is not None, "MCMC line not found or formatted incorrectly in results.txt."

    ols_b0 = float(ols_match.group(1))
    ols_b1 = float(ols_match.group(2))
    ols_b2 = float(ols_match.group(3))

    mcmc_b0 = float(mcmc_match.group(1))
    mcmc_b1 = float(mcmc_match.group(2))
    mcmc_b2 = float(mcmc_match.group(3))

    # Expected OLS values based on the deterministic data generation
    expected_ols_b0 = 1.4883
    expected_ols_b1 = -0.8268
    expected_ols_b2 = 0.2037

    # Check OLS values
    assert abs(ols_b0 - expected_ols_b0) < 0.005, f"OLS beta0 is incorrect: {ols_b0}"
    assert abs(ols_b1 - expected_ols_b1) < 0.005, f"OLS beta1 is incorrect: {ols_b1}"
    assert abs(ols_b2 - expected_ols_b2) < 0.005, f"OLS beta2 is incorrect: {ols_b2}"

    # Check MCMC values (should be close to OLS values)
    assert abs(mcmc_b0 - ols_b0) < 0.1, f"MCMC beta0 ({mcmc_b0}) is too far from OLS beta0 ({ols_b0})"
    assert abs(mcmc_b1 - ols_b1) < 0.1, f"MCMC beta1 ({mcmc_b1}) is too far from OLS beta1 ({ols_b1})"
    assert abs(mcmc_b2 - ols_b2) < 0.1, f"MCMC beta2 ({mcmc_b2}) is too far from OLS beta2 ({ols_b2})"