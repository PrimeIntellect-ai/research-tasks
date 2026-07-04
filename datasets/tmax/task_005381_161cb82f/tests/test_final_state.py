# test_final_state.py

import os
import math
import pytest

def test_source_code_exists():
    """Check that the C++ source code file exists."""
    src_path = "/home/user/src/rms_calc.cpp"
    assert os.path.isfile(src_path), f"Source file {src_path} does not exist."

def test_executable_exists_and_runnable():
    """Check that the compiled executable exists and has execute permissions."""
    bin_path = "/home/user/bin/rms_calc"
    assert os.path.isfile(bin_path), f"Executable {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_rms_result_correct():
    """Compute the expected RMS from the PDB file and verify the program output."""
    pdb_path = "/home/user/data/molecule.pdb"
    result_path = "/home/user/output/rms_result.txt"

    assert os.path.isfile(pdb_path), f"PDB file {pdb_path} is missing."
    assert os.path.isfile(result_path), f"Result file {result_path} is missing."

    # Calculate truth RMS from the actual PDB file
    sum_sq = 0.0
    count = 0
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM  '):
                # X: 31-38 (index 30:38), Y: 39-46 (index 38:46), Z: 47-54 (index 46:54)
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                sum_sq += x*x + y*y + z*z
                count += 1

    assert count > 0, "No ATOM records found in the PDB file."
    expected_rms = math.sqrt(sum_sq / count)
    expected_str = f"RMS: {expected_rms:.4f}"

    with open(result_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_str, (
        f"Incorrect RMS result in {result_path}. "
        f"Expected '{expected_str}', got '{actual_content}'."
    )

def test_analytical_result_correct():
    """Verify the analytical expected value is correctly written."""
    analytical_path = "/home/user/output/analytical.txt"
    assert os.path.isfile(analytical_path), f"Analytical result file {analytical_path} is missing."

    # The theoretical RMS for uniform distribution in [-10, 10]^3 is exactly 10.0000
    expected_analytical = "Expected: 10.0000"

    with open(analytical_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_analytical, (
        f"Incorrect analytical result in {analytical_path}. "
        f"Expected '{expected_analytical}', got '{actual_content}'."
    )