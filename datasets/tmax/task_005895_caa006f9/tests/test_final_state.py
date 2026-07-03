# test_final_state.py

import os
import sys
import pytest

def test_parallel_mcmc_script_exists():
    script_path = '/home/user/parallel_mcmc.py'
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."

def test_final_k_file_exists():
    file_path = '/home/user/final_k.txt'
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

def test_final_k_value():
    sys.path.insert(0, '/home/user')
    try:
        from mcmc_ode import run_mcmc
    except ImportError:
        pytest.fail("Could not import run_mcmc from /home/user/mcmc_ode.py")

    # Compute the expected value
    res = []
    for s in [42, 43, 44, 45]:
        res.append(run_mcmc(s))
    expected_k = sum(res) / 4.0
    expected_str = f"{expected_k:.4f}"

    # Read the actual value
    file_path = '/home/user/final_k.txt'
    with open(file_path, 'r') as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected final k value to be '{expected_str}', but got '{actual_str}'"