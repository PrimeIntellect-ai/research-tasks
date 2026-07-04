# test_final_state.py

import os
import pytest

def test_mcmc_fit_script_exists():
    """Test that the python script was created."""
    script_path = '/home/user/mcmc_fit.py'
    assert os.path.isfile(script_path), f"Expected script not found at {script_path}"

def test_results_file_exists_and_correct():
    """Test that the results.txt file exists and contains correct values."""
    results_path = '/home/user/results.txt'
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    with open(results_path, 'r') as f:
        content = f.read().strip()

    assert content, "The results.txt file is empty."

    parts = content.split(',')
    assert len(parts) == 2, f"Expected format 'A_mean,f_mean', but got '{content}'"

    try:
        a_mean = float(parts[0])
        f_mean = float(parts[1])
    except ValueError:
        pytest.fail(f"Could not parse floats from results.txt content: '{content}'")

    assert 2.34 <= a_mean <= 2.44, f"A_mean {a_mean} is outside the acceptable range [2.34, 2.44]"
    assert 3.65 <= f_mean <= 3.75, f"f_mean {f_mean} is outside the acceptable range [3.65, 3.75]"