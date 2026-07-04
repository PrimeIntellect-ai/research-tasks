# test_final_state.py

import os
import pytest

def test_mcmc_degrade_c_fixed():
    file_path = "/home/user/mcmc_degrade.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."
    with open(file_path, 'r') as f:
        content = f.read()

    assert "double dt = 0.01;" in content, "The step size 'dt' was not updated to 0.01 in mcmc_degrade.c."
    assert "double dt = 2.0;" not in content, "The buggy step size 'dt = 2.0;' is still present in mcmc_degrade.c."

def test_run_pipeline_exists():
    file_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(file_path), f"Script {file_path} is missing."

def test_posterior_mean_value():
    file_path = "/home/user/posterior_mean.txt"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. Did the pipeline run correctly?"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content in ["0.299", "0.300", "0.301"], f"Expected posterior mean to be 0.299, 0.300, or 0.301, but got '{content}'."