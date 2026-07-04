# test_final_state.py

import os
import re

def test_results_file_exists():
    """Check if the results.txt file exists."""
    file_path = "/home/user/results.txt"
    assert os.path.exists(file_path), f"File not found: {file_path}"
    assert os.path.isfile(file_path), f"Path is not a file: {file_path}"

def test_results_content_and_values():
    """Parse results.txt and validate the mathematical bounds of the results."""
    file_path = "/home/user/results.txt"
    with open(file_path, "r") as f:
        content = f.read()

    mcmc_match = re.search(r"MCMC_Lambda_Mean:\s*([0-9.]+)", content)
    ci_lower_match = re.search(r"Bootstrap_CI_Lower:\s*([0-9.]+)", content)
    ci_upper_match = re.search(r"Bootstrap_CI_Upper:\s*([0-9.]+)", content)

    assert mcmc_match, "Results file is missing 'MCMC_Lambda_Mean: <value>'"
    assert ci_lower_match, "Results file is missing 'Bootstrap_CI_Lower: <value>'"
    assert ci_upper_match, "Results file is missing 'Bootstrap_CI_Upper: <value>'"

    mcmc_mean = float(mcmc_match.group(1))
    ci_lower = float(ci_lower_match.group(1))
    ci_upper = float(ci_upper_match.group(1))

    # Based on analytical sample mean of 0.14
    assert 0.10 <= mcmc_mean <= 0.18, f"MCMC Mean {mcmc_mean} out of bounds (expected ~0.14)."
    assert 0.02 <= ci_lower <= 0.10, f"CI Lower {ci_lower} out of bounds (expected ~0.04)."
    assert 0.20 <= ci_upper <= 0.30, f"CI Upper {ci_upper} out of bounds (expected ~0.26)."