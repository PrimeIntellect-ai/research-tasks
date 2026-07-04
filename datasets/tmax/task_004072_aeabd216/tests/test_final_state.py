# test_final_state.py

import os
import re

def test_pipeline_script_exists_and_executable():
    """Check that run_pipeline.sh exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_cpp_source_exists():
    """Check that posterior_estimation.cpp exists."""
    cpp_path = "/home/user/posterior_estimation.cpp"
    assert os.path.exists(cpp_path), f"{cpp_path} does not exist."

def test_results_file_and_values():
    """Check that results.txt exists, has the correct format, and values are mathematically sound."""
    results_path = "/home/user/results.txt"
    assert os.path.exists(results_path), f"{results_path} does not exist."

    with open(results_path, "r") as f:
        content = f.read()

    # Parse values
    map_mu_match = re.search(r"MAP_MU:\s*([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)", content)
    mcmc_mean_match = re.search(r"MCMC_MEAN:\s*([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)", content)
    mcmc_var_match = re.search(r"MCMC_VAR:\s*([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)", content)

    assert map_mu_match is not None, "Could not find MAP_MU in results.txt"
    assert mcmc_mean_match is not None, "Could not find MCMC_MEAN in results.txt"
    assert mcmc_var_match is not None, "Could not find MCMC_VAR in results.txt"

    map_mu = float(map_mu_match.group(1))
    mcmc_mean = float(mcmc_mean_match.group(1))
    mcmc_var = float(mcmc_var_match.group(1))

    # Theoretical posterior variance is approx 0.02
    assert abs(mcmc_var - 0.02) < 0.005, f"MCMC_VAR ({mcmc_var}) is not close to theoretical variance 0.02."

    # MAP and MCMC mean should be very close to each other
    assert abs(map_mu - mcmc_mean) < 0.01, f"MAP_MU ({map_mu}) and MCMC_MEAN ({mcmc_mean}) differ by more than 0.01."

    # Both means should be reasonably close to the true parameter 5.0
    assert abs(map_mu - 5.0) < 0.5, f"MAP_MU ({map_mu}) is not close enough to the true parameter 5.0."