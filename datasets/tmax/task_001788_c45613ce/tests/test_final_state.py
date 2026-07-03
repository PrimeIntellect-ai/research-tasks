# test_final_state.py
import os
import re

def test_posterior_results_file():
    """Check if the posterior_results.txt file exists and contains the correct deterministic values."""
    results_file = "/home/user/posterior_results.txt"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist. Did you run the script?"

    with open(results_file, "r") as f:
        content = f.read().strip()

    assert "alpha: 2.4939" in content, f"Expected 'alpha: 2.4939' not found in results. Found: {content}"
    assert "beta: 0.4990" in content, f"Expected 'beta: 0.4990' not found in results. Found: {content}"

def test_script_fixed():
    """Check if the script was modified to fix the non-deterministic iteration."""
    script_file = "/home/user/fit_mcmc.py"
    assert os.path.isfile(script_file), f"Script file {script_file} does not exist."

    with open(script_file, "r") as f:
        content = f.read()

    # The script should sort the sequence identifiers to ensure deterministic iteration.
    # We check that the sorting logic is present or the buggy set iteration is removed.
    has_sorted = "sorted(" in content
    has_buggy_set = "unique_seqs = set(data.keys())" in content and "for seq in unique_seqs:" in content

    assert has_sorted or not has_buggy_set, \
        "The script still appears to iterate over an unordered set. You must sort the sequence identifiers."