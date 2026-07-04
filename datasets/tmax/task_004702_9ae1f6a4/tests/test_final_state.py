# test_final_state.py

import os
import subprocess
import pytest

def test_compute_deriv_sh():
    path = "/home/user/compute_deriv.sh"
    assert os.path.exists(path), f"Missing script: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

def test_test_pipeline_sh():
    path = "/home/user/test_pipeline.sh"
    assert os.path.exists(path), f"Missing script: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

    # Run the test pipeline script
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"test_pipeline.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_sim_max_deriv_txt():
    output_path = "/home/user/sim_max_deriv.txt"
    secret_path = "/home/user/.sim_expected_secret.txt"

    assert os.path.exists(output_path), f"Missing output file: {output_path}"
    assert os.path.exists(secret_path), f"Missing secret file: {secret_path}"

    with open(output_path, 'r') as f:
        actual = f.read().strip()

    with open(secret_path, 'r') as f:
        expected = f.read().strip()

    assert actual == expected, f"Output in {output_path} does not match expected value. Expected '{expected}', got '{actual}'."