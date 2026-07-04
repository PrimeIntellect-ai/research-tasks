# test_final_state.py
import os
import subprocess
import tempfile
import pytest

def test_stencil_cpp_fixes():
    """Test that stencil.cpp is fixed and produces correct output."""
    cpp_path = "/home/user/stencil.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        bin_path = os.path.join(tmpdir, "stencil")

        # Compile the modified C++ code
        compile_cmd = ["g++", "-O2", cpp_path, "-o", bin_path]
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Compilation failed:\n{result.stderr}"

        # Run for N=100
        run_cmd = [bin_path, "100"]
        result = subprocess.run(run_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Execution failed for N=100:\n{result.stderr}"

        output = result.stdout.strip()
        try:
            error_val = float(output)
        except ValueError:
            pytest.fail(f"Could not parse output as float: {output}")

        assert error_val < 0.002, f"Error for N=100 is {error_val}, expected < 0.002. The bug might not be fully fixed."

def test_errors_txt():
    """Test that errors.txt contains the correct convergence results."""
    txt_path = "/home/user/errors.txt"
    assert os.path.isfile(txt_path), f"File {txt_path} does not exist."

    with open(txt_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in errors.txt, found {len(lines)}."

    expected_values = [0.162319, 0.040989, 0.010265, 0.002568]

    for i, (line, expected) in enumerate(zip(lines, expected_values)):
        try:
            val = float(line)
        except ValueError:
            pytest.fail(f"Line {i+1} in errors.txt is not a valid float: {line}")

        assert abs(val - expected) < 1e-4, f"Value on line {i+1} is {val}, expected approximately {expected}."