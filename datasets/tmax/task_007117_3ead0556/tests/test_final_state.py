# test_final_state.py

import os
import pytest

def test_mcmc_py_exists():
    """Check if the mcmc.py script was created."""
    script_path = "/home/user/mcmc.py"
    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} is not a regular file."

def test_mcmc_gc_mean_txt():
    """Check if mcmc_gc_mean.txt exists and contains a valid mean within the expected range."""
    output_path = "/home/user/mcmc_gc_mean.txt"
    assert os.path.exists(output_path), f"The output file {output_path} is missing."
    assert os.path.isfile(output_path), f"The path {output_path} is not a regular file."

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content, f"The file {output_path} is empty."

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"The content of {output_path} ('{content}') cannot be parsed as a float.")

    assert 0.540 <= val <= 0.555, f"The estimated mean {val} is outside the acceptable range [0.540, 0.555]."