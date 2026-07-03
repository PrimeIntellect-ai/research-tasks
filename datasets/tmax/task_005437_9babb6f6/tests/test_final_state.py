# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_eigen_fixed():
    math_functions_path = "/app/vendor/eigen/Eigen/src/Core/MathFunctions.h"
    assert os.path.isfile(math_functions_path), f"{math_functions_path} is missing"
    with open(math_functions_path, "r") as f:
        content = f.read()
    assert "Deliberate perturbation" not in content, "Vendored package not fixed: perturbation still present in MathFunctions.h"

def test_executable_exists():
    executable = "/home/user/filter"
    assert os.path.isfile(executable), f"Executable {executable} not found"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable"

def test_clean_corpus():
    executable = "/home/user/filter"
    clean_files = glob.glob("/home/user/corpora/clean/*")
    assert len(clean_files) > 0, "No clean corpus files found"

    failed_files = []
    for f in clean_files:
        result = subprocess.run([executable, f], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}"

def test_evil_corpus():
    executable = "/home/user/filter"
    evil_files = glob.glob("/home/user/corpora/evil/*")
    assert len(evil_files) > 0, "No evil corpus files found"

    failed_files = []
    for f in evil_files:
        result = subprocess.run([executable, f], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed/accepted: {', '.join(failed_files)}"