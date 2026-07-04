# test_final_state.py

import os
import subprocess
import pytest

def test_executables_exist():
    """Test that the required executables were created and are executable."""
    strict_path = "/home/user/seq_strict"
    fast_path = "/home/user/seq_fast"

    assert os.path.isfile(strict_path), f"The executable {strict_path} does not exist."
    assert os.access(strict_path, os.X_OK), f"The file {strict_path} is not executable."

    assert os.path.isfile(fast_path), f"The executable {fast_path} does not exist."
    assert os.access(fast_path, os.X_OK), f"The file {fast_path} is not executable."

def test_max_diff_correct():
    """Test that max_diff.txt contains the correct maximum absolute difference."""
    max_diff_path = "/home/user/max_diff.txt"
    source_path = "/home/user/seq_sim.c"

    assert os.path.isfile(max_diff_path), f"The file {max_diff_path} does not exist."

    # Independently compile to verify the truth
    tmp_strict = "/tmp/seq_strict_truth"
    tmp_fast = "/tmp/seq_fast_truth"

    subprocess.run(["gcc", "-O0", source_path, "-o", tmp_strict], check=True)
    subprocess.run(["gcc", "-O3", "-ffast-math", source_path, "-o", tmp_fast], check=True)

    # Run both and capture output
    out_strict = subprocess.run([tmp_strict], capture_output=True, text=True, check=True).stdout.strip().split('\n')
    out_fast = subprocess.run([tmp_fast], capture_output=True, text=True, check=True).stdout.strip().split('\n')

    # Calculate maximum absolute difference
    max_diff = 0.0
    for s_line, f_line in zip(out_strict, out_fast):
        if not s_line or not f_line:
            continue
        # Format is "A: 0.25xxxxxx"
        s_val = float(s_line.split(':')[1].strip())
        f_val = float(f_line.split(':')[1].strip())
        diff = abs(s_val - f_val)
        if diff > max_diff:
            max_diff = diff

    expected_diff_str = f"{max_diff:.8f}"

    # Read student's output
    with open(max_diff_path, "r") as f:
        actual_diff_str = f.read().strip()

    assert actual_diff_str == expected_diff_str, (
        f"Incorrect value in {max_diff_path}. "
        f"Expected {expected_diff_str}, but got '{actual_diff_str}'."
    )