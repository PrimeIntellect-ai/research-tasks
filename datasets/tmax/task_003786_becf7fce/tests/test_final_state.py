# test_final_state.py

import os
import pytest

def test_compiled_binary_exists():
    """Test that the C program was compiled to the specified path and is executable."""
    binary_path = "/home/user/thermal_sim"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Compiled binary at {binary_path} is not executable"

def test_bash_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    script_path = "/home/user/solve_time.sh"
    assert os.path.isfile(script_path), f"Bash script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Bash script at {script_path} is not executable"

def test_result_file_content():
    """Test that the result file exists and contains the correct formatted value."""
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file not found at {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content == "1.0136", f"Expected result '1.0136', but got '{content}'"