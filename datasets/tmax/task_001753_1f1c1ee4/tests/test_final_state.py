# test_final_state.py

import os
import re
import pytest

def test_results_file_exists():
    """Check that the results file exists."""
    results_file = "/home/user/results.txt"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

def test_results_content():
    """Check the contents of the results file for correct analytical and MCMC values."""
    results_file = "/home/user/results.txt"
    assert os.path.isfile(results_file), "Results file missing."

    with open(results_file, "r") as f:
        content = f.read()

    # Parse Analytical Mean
    match = re.search(r"Analytical Mean:\s*([0-9\.]+)", content)
    assert match is not None, "Could not find 'Analytical Mean:' in results.txt"
    analytical_mean = float(match.group(1))
    assert abs(analytical_mean - 106.0488) < 1e-4, f"Analytical Mean incorrect. Expected ~106.0488, got {analytical_mean}"

    # Parse Analytical Variance
    match = re.search(r"Analytical Variance:\s*([0-9\.]+)", content)
    assert match is not None, "Could not find 'Analytical Variance:' in results.txt"
    analytical_var = float(match.group(1))
    assert abs(analytical_var - 9.7561) < 1e-4, f"Analytical Variance incorrect. Expected ~9.7561, got {analytical_var}"

    # Parse MCMC Mean
    match = re.search(r"MCMC Mean:\s*([0-9\.]+)", content)
    assert match is not None, "Could not find 'MCMC Mean:' in results.txt"
    mcmc_mean = float(match.group(1))
    assert 105.9 <= mcmc_mean <= 106.2, f"MCMC Mean {mcmc_mean} is out of expected range [105.9, 106.2]"

    # Parse MCMC Variance
    match = re.search(r"MCMC Variance:\s*([0-9\.]+)", content)
    assert match is not None, "Could not find 'MCMC Variance:' in results.txt"
    mcmc_var = float(match.group(1))
    assert 9.2 <= mcmc_var <= 10.3, f"MCMC Variance {mcmc_var} is out of expected range [9.2, 10.3]"

    # Parse P(mu > 105)
    match = re.search(r"P\(mu > 105\):\s*([0-9\.]+)", content)
    assert match is not None, "Could not find 'P(mu > 105):' in results.txt"
    p_mu = float(match.group(1))
    assert 0.6000 <= p_mu <= 0.6600, f"P(mu > 105) {p_mu} is out of expected range [0.6000, 0.6600]"