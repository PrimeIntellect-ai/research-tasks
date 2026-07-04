# test_final_state.py

import os
import pytest

def test_fixed_output_exists():
    """Check if the expected output file exists."""
    output_path = "/home/user/fixed_output.txt"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

def test_fixed_output_content():
    """Check if the expected output file contains the correct trajectory value."""
    output_path = "/home/user/fixed_output.txt"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = "Trajectory: 140.4304968"
    assert content == expected_content, f"Output file content is incorrect. Expected '{expected_content}', got '{content}'."

def test_executable_exists():
    """Check if the compiled executable exists."""
    exe_path = "/home/user/astro_calc/astro_calc"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist. Ensure the project was compiled."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."