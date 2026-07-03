# test_final_state.py

import os
import math
import stat
import subprocess
import pytest

def test_binary_exists():
    binary_path = "/home/user/compute_spectrum"
    assert os.path.isfile(binary_path), f"Compiled binary missing at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable"

def test_check_stability_script():
    script_path = "/home/user/check_stability.sh"
    assert os.path.isfile(script_path), f"Stability script missing at {script_path}"

    # Check executable permission
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} must be executable"

    # Run the script and check exit code
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"check_stability.sh failed with exit code {result.returncode}. Output: {result.stdout} {result.stderr}"

def test_output_matches_reference():
    avg_path = "/home/user/avg_spectrum.txt"
    ref_path = "/home/user/reference_spectrum.txt"

    assert os.path.isfile(avg_path), f"Output file missing at {avg_path}"
    assert os.path.isfile(ref_path), f"Reference file missing at {ref_path}"

    with open(avg_path, "r") as f:
        avg_lines = [line.strip() for line in f if line.strip()]

    with open(ref_path, "r") as f:
        ref_lines = [line.strip() for line in f if line.strip()]

    assert len(avg_lines) == len(ref_lines), "Output file does not have the same number of lines as the reference file."

    for i, (avg_str, ref_str) in enumerate(zip(avg_lines, ref_lines)):
        try:
            avg_val = float(avg_str)
            ref_val = float(ref_str)
        except ValueError:
            pytest.fail(f"Could not parse line {i+1} as float: '{avg_str}' or '{ref_str}'")

        assert math.isclose(avg_val, ref_val, rel_tol=1e-9, abs_tol=1e-12), \
            f"Value mismatch at line {i+1}: expected {ref_val}, got {avg_val}"

def test_cpp_modifications():
    cpp_path = "/home/user/compute_spectrum.cpp"
    assert os.path.isfile(cpp_path), f"Source code missing at {cpp_path}"

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "double" in content, "The source code should use 'double' precision for calculations."
    assert "#pragma omp atomic" not in content, "The source code should not use '#pragma omp atomic' to avoid non-deterministic reduction order."