# test_final_state.py
import os
import pytest

def test_optimizer_script_exists_and_executable():
    """Test that the bash script optimizer.sh exists and is executable."""
    script_path = "/home/user/optimizer.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist or is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_optimal_p_file_exists_and_correct():
    """Test that optimal_p.txt exists and contains the correct optimized value."""
    output_path = "/home/user/optimal_p.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "14.68", f"Expected the file {output_path} to contain exactly '14.68', but got '{content}'."