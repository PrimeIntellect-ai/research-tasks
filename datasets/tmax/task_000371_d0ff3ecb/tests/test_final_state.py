# test_final_state.py
import os
import json

def test_mcmc_sampler_script_exists():
    """Check that the script mcmc_sampler.py exists."""
    script_path = "/home/user/mcmc_sampler.py"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_posterior_summary_exists_and_valid():
    """Check that posterior_summary.json exists and contains the correct values."""
    summary_path = "/home/user/posterior_summary.json"
    assert os.path.exists(summary_path), f"Output file {summary_path} is missing."
    assert os.path.isfile(summary_path), f"{summary_path} is not a file."

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{summary_path} does not contain valid JSON."

    expected_analytical = 72 / 104.0

    assert "analytical_mean" in data, "Key 'analytical_mean' is missing from the JSON."
    assert "mcmc_mean" in data, "Key 'mcmc_mean' is missing from the JSON."
    assert "samples_kept" in data, "Key 'samples_kept' is missing from the JSON."

    assert abs(data['analytical_mean'] - expected_analytical) < 1e-5, \
        f"Analytical mean incorrect: expected approx {expected_analytical:.6f}, got {data['analytical_mean']}"

    assert abs(data['mcmc_mean'] - expected_analytical) < 0.005, \
        f"MCMC mean out of bounds: expected within 0.005 of {expected_analytical:.6f}, got {data['mcmc_mean']}"

    assert data['samples_kept'] == 100000, \
        f"Incorrect number of samples kept: expected 100000, got {data['samples_kept']}"