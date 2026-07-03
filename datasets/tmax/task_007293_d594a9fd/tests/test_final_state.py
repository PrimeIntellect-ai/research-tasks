# test_final_state.py

import os
import subprocess
import math

def test_c_program_exists():
    """Check that the C program exists."""
    assert os.path.isfile('/home/user/svd_sim.c'), "/home/user/svd_sim.c does not exist"

def test_pipeline_script_exists_and_executable():
    """Check that the pipeline script exists and is executable."""
    script_path = '/home/user/pipeline.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_pipeline_execution_and_outputs():
    """Run the pipeline script and verify the outputs."""
    script_path = '/home/user/pipeline.sh'

    # Run the script
    result = subprocess.run([script_path], cwd='/home/user', capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Calculate expected value dynamically
    # norm_spatial
    sum_spatial_sq = 0.0
    for x in range(100):
        for y in range(100):
            val = math.sin(math.pi * x / 100.0) * math.cos(math.pi * y / 100.0)
            sum_spatial_sq += val * val
    norm_spatial = math.sqrt(sum_spatial_sq)

    # norm_temporal
    sum_temporal_sq = 0.0
    for t in range(10):
        val = math.exp(-0.1 * t)
        sum_temporal_sq += val * val
    norm_temporal = math.sqrt(sum_temporal_sq)

    expected_sigma = norm_spatial * norm_temporal
    expected_str = f"{expected_sigma:.4f}"

    # Check singular_value.txt
    sv_path = '/home/user/singular_value.txt'
    assert os.path.isfile(sv_path), f"{sv_path} was not created"
    with open(sv_path, 'r') as f:
        sv_content = f.read().strip()

    assert sv_content == expected_str, f"Expected singular value {expected_str}, but got {sv_content}"

    # Check notebook.md
    nb_path = '/home/user/notebook.md'
    assert os.path.isfile(nb_path), f"{nb_path} was not created"
    with open(nb_path, 'r') as f:
        nb_content = f.read()

    expected_nb_string = f"The dominant singular value is: {expected_str}"
    assert expected_nb_string in nb_content, f"Expected string '{expected_nb_string}' not found in {nb_path}"