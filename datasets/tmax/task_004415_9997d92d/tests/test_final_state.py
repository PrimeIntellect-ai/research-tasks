# test_final_state.py

import os
import json
import math

def test_files_exist():
    """Verify that the required files have been created."""
    assert os.path.isfile("/home/user/mcmc_pipeline.cpp"), "Source file /home/user/mcmc_pipeline.cpp is missing."
    assert os.path.isfile("/home/user/mcmc_pipeline"), "Compiled binary /home/user/mcmc_pipeline is missing."
    assert os.path.isfile("/home/user/results.json"), "Results file /home/user/results.json is missing."

def test_json_structure_and_values():
    """Verify the contents and numerical accuracy of results.json."""
    with open("/home/user/results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not a valid JSON file."

    # Check keys
    required_keys = ["empirical_mu", "empirical_cov", "kl_divergence"]
    for key in required_keys:
        assert key in data, f"Missing required key '{key}' in results.json."

    emp_mu = data["empirical_mu"]
    emp_cov = data["empirical_cov"]
    kl_div = data["kl_divergence"]

    # Validate structure
    assert isinstance(emp_mu, list) and len(emp_mu) == 2, "empirical_mu must be a list of 2 elements."
    assert isinstance(emp_cov, list) and len(emp_cov) == 2, "empirical_cov must be a 2x2 matrix."
    assert all(isinstance(row, list) and len(row) == 2 for row in emp_cov), "empirical_cov must be a 2x2 matrix."
    assert isinstance(kl_div, (int, float)), "kl_divergence must be a number."

    # True values
    mu_true = [1.0, 2.0]
    cov_true = [[2.0, 0.5], [0.5, 1.0]]

    # Check empirical mean
    for i in range(2):
        assert math.isclose(emp_mu[i], mu_true[i], abs_tol=0.1), \
            f"Empirical mean at index {i} ({emp_mu[i]}) is too far from true mean ({mu_true[i]})."

    # Check empirical covariance
    for i in range(2):
        for j in range(2):
            assert math.isclose(emp_cov[i][j], cov_true[i][j], abs_tol=0.2), \
                f"Empirical covariance at [{i}][{j}] ({emp_cov[i][j]}) is too far from true covariance ({cov_true[i][j]})."

    # Check KL divergence
    assert 0 <= kl_div <= 0.05, f"KL divergence {kl_div} is out of expected bounds [0, 0.05]."

def test_source_code_requirements():
    """Verify that the C++ code uses Cholesky Decomposition (LLT)."""
    with open("/home/user/mcmc_pipeline.cpp", "r") as f:
        code = f.read()

    # Check for LLT usage
    has_llt = "llt()" in code or "LLT" in code
    assert has_llt, "Cholesky decomposition (LLT) not found in source code. You must use Eigen's LLT."