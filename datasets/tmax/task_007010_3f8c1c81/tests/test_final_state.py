# test_final_state.py

import os
import subprocess
import pytest

def test_src_exists_and_openmp():
    """Check if the C source file exists and contains OpenMP pragmas."""
    src_file = "/home/user/src/prepare_dataset.c"
    assert os.path.isfile(src_file), f"Source file {src_file} does not exist."

    with open(src_file, "r") as f:
        content = f.read()

    assert "#pragma omp" in content, f"Source file {src_file} is missing OpenMP pragmas ('#pragma omp')."

def test_bin_exists_and_linked_openmp():
    """Check if the compiled binary exists, is executable, and is linked with OpenMP."""
    bin_file = "/home/user/bin/prepare_dataset"
    assert os.path.isfile(bin_file), f"Binary file {bin_file} does not exist."
    assert os.access(bin_file, os.X_OK), f"Binary file {bin_file} is not executable."

    # Check if linked with libgomp
    result = subprocess.run(["ldd", bin_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Running ldd on {bin_file} failed."
    assert "libgomp" in result.stdout, f"Binary {bin_file} is not linked with libgomp. Ensure you compiled with -fopenmp."

def test_csv_output():
    """Check if the output CSV matches the expected format and values."""
    csv_file = "/home/user/output/ml_features.csv"
    assert os.path.isfile(csv_file), f"Output file {csv_file} does not exist."

    expected_content = (
        "SeqID,PurineRatio,ObservationLabel\n"
        "seq001,0.5000,0.98\n"
        "seq002,0.4667,0.45\n"
        "seq003,0.5000,1.23\n"
        "seq004,0.5000,0.11\n"
        "seq005,0.5000,0.76\n"
    )

    with open(csv_file, "r") as f:
        actual_content = f.read()

    # Strip trailing newlines for a more robust comparison
    assert actual_content.strip() == expected_content.strip(), (
        f"Contents of {csv_file} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )