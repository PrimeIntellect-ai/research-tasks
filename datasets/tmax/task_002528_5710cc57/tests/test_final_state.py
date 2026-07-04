# test_final_state.py
import os
import math
import pytest

def test_fast_analysis_c_exists():
    """Test that the C source file exists."""
    assert os.path.isfile("/home/user/fast_analysis.c"), "The file /home/user/fast_analysis.c does not exist."

def test_fast_analysis_executable_exists():
    """Test that the compiled executable exists."""
    assert os.path.isfile("/home/user/fast_analysis"), "The compiled executable /home/user/fast_analysis does not exist."
    assert os.access("/home/user/fast_analysis", os.X_OK), "The file /home/user/fast_analysis is not executable."

def test_stat_result():
    """Test that the stat_result.txt contains the correct Z-score."""
    pdb_file = "/home/user/data.pdb"
    result_file = "/home/user/stat_result.txt"

    assert os.path.isfile(pdb_file), f"Missing required file: {pdb_file}"
    assert os.path.isfile(result_file), f"The result file {result_file} does not exist."

    n1 = 0
    n2 = 0
    sum_z1 = 0.0
    sum_z2 = 0.0

    with open(pdb_file, "r") as f:
        for line in f:
            if line.startswith("ATOM"):
                x = float(line[30:38].strip())
                z = float(line[46:54].strip())
                if x >= 0:
                    n1 += 1
                    sum_z1 += z
                else:
                    n2 += 1
                    sum_z2 += z

    assert n1 > 0, "No atoms found in Domain 1 (X >= 0.0)"
    assert n2 > 0, "No atoms found in Domain 2 (X < 0.0)"

    mu1 = sum_z1 / n1
    mu2 = sum_z2 / n2
    expected_z_score = (mu1 - mu2) / math.sqrt(1.0/n1 + 1.0/n2)
    expected_output = f"Z-score: {expected_z_score:.3f}"

    with open(result_file, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Expected '{expected_output}', but got '{actual_output}' in {result_file}"