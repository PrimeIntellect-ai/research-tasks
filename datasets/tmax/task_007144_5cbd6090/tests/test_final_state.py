# test_final_state.py

import os
import re
import pytest

def test_eigen_installed():
    header_path = "/home/user/eigen/Eigen/Dense"
    assert os.path.exists(header_path), f"Eigen headers not found at {header_path}"

def test_cpp_code_exists():
    cpp_path = "/home/user/process_logs.cpp"
    assert os.path.exists(cpp_path), f"C++ source code not found at {cpp_path}"

def test_binary_exists():
    bin_path = "/home/user/process_logs"
    assert os.path.exists(bin_path), f"Compiled binary not found at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"File at {bin_path} is not executable"

def test_output_file_exists_and_correct():
    out_path = "/home/user/output/ci.txt"
    assert os.path.exists(out_path), f"Output file not found at {out_path}"

    with open(out_path, "r") as f:
        content = f.read().strip()

    match = re.search(r"Lower:\s*([\d.]+),\s*Upper:\s*([\d.]+)", content)
    assert match is not None, f"Output format incorrect. Expected 'Lower: <value>, Upper: <value>', got: {content}"

    lower = float(match.group(1))
    upper = float(match.group(2))

    # The expected values are around Lower: ~0.54, Upper: ~1.26 depending on the exact sequence
    # Allow a reasonable range to account for potential standard library variations in uniform_int_distribution
    assert 0.4 <= lower <= 0.7, f"Lower bound {lower} is outside expected range [0.4, 0.7]"
    assert 1.1 <= upper <= 1.5, f"Upper bound {upper} is outside expected range [1.1, 1.5]"