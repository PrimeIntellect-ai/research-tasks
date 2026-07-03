# test_final_state.py

import os
import re

def test_result_txt_exists_and_correct():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the program and redirect output?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "KL Divergence: 2.0191"
    assert expected in content, f"Expected output '{expected}' not found in {path}. Found: '{content}'"

def test_executable_exists():
    path = "/home/user/kmer_dist"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the C program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_c_code_contains_openmp_fixes():
    path = "/home/user/kmer_dist.c"
    assert os.path.isfile(path), f"Source file {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check that OpenMP is still used
    assert "#pragma omp parallel" in content or "_Pragma" in content, "OpenMP parallel directive is missing from the code."

    # Check for race condition fix (atomic, critical, or reduction)
    has_atomic = "atomic" in content
    has_critical = "critical" in content
    has_reduction = "reduction" in content
    has_locks = "omp_set_lock" in content

    assert any([has_atomic, has_critical, has_reduction, has_locks]), "No OpenMP synchronization (atomic, critical, reduction, or locks) found to fix the race condition."

def test_c_code_contains_smoothing():
    path = "/home/user/kmer_dist.c"
    with open(path, "r") as f:
        content = f.read()

    # Check for 1e-6 smoothing
    assert "1e-6" in content or "0.000001" in content, "Additive smoothing of 1e-6 is not found in the code."