# test_final_state.py

import os
import math

PROJECT_DIR = "/home/user/project"

def test_makefile_fixed_and_lib_built():
    so_path = os.path.join(PROJECT_DIR, "libmathcodec.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built."

def test_python_script_exists():
    py_path = os.path.join(PROJECT_DIR, "test_codec.py")
    assert os.path.isfile(py_path), f"Python script {py_path} does not exist."

def test_python_test_out():
    out_path = os.path.join(PROJECT_DIR, "python_test_out.txt")
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist."

    with open(out_path, "r") as f:
        content = f.read().strip()

    # Expected: "9.165, 9.307, 10.695, 11.165"
    expected_vals = []
    for i, char in enumerate("TEST"):
        val = math.sqrt(ord(char)) + math.log2(i + 1)
        expected_vals.append(f"{val:.3f}")

    expected_str = ", ".join(expected_vals)

    # Allow some flexibility in formatting (e.g., without spaces)
    normalized_content = content.replace(" ", "")
    normalized_expected = expected_str.replace(" ", "")

    assert normalized_content == normalized_expected, f"python_test_out.txt content mismatch. Expected something like {expected_str}, got {content}"

def test_go_processor_built():
    bin_path = os.path.join(PROJECT_DIR, "processor")
    assert os.path.isfile(bin_path), f"Go binary {bin_path} was not built."
    assert os.access(bin_path, os.X_OK), f"Go binary {bin_path} is not executable."

def test_go_processor_output():
    out_path = os.path.join(PROJECT_DIR, "output.txt")
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist."

    with open(out_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n")]

    assert len(lines) == 4, f"Expected 4 lines in output.txt, got {len(lines)}"

    # Calculate expected first line for "HELLO"
    expected_hello = []
    for i, char in enumerate("HELLO"):
        val = math.sqrt(ord(char)) + math.log2(i + 1)
        expected_hello.append(f"{val:.2f}")

    expected_line = " ".join(expected_hello)

    assert lines[0] == expected_line, f"First line of output.txt mismatch. Expected '{expected_line}', got '{lines[0]}'"