# test_final_state.py

import os
import subprocess
import pytest

def test_c_code_fixed():
    c_file = "/home/user/project/c_src/libevaluator.c"
    assert os.path.isfile(c_file), f"File {c_file} is missing."
    with open(c_file, "r") as f:
        content = f.read()

    # The bug was "return a + b; // BUG: should be a * b" for op_code == 2
    # We should check that it now does multiplication.
    # A simple heuristic: check if there's a return a * b;
    assert "a * b" in content, "The C code does not seem to have been fixed to perform multiplication (a * b)."

def test_makefile_fixed():
    makefile = "/home/user/project/c_src/Makefile"
    assert os.path.isfile(makefile), f"File {makefile} is missing."
    with open(makefile, "r") as f:
        content = f.read()

    assert "-fPIC" in content, "Makefile is missing the -fPIC flag."
    assert "-shared" in content, "Makefile is missing the -shared flag."

def test_library_built():
    so_file = "/home/user/project/c_src/libevaluator.so"
    assert os.path.isfile(so_file), f"Shared library {so_file} was not built."

    # Check if it's a valid ELF shared object
    with open(so_file, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{so_file} is not a valid ELF file."

def test_results_correct():
    results_file = "/home/user/project/results.txt"
    assert os.path.isfile(results_file), f"Results file {results_file} is missing."

    with open(results_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["42", "58", "72", "12", "-30", "0"]
    assert lines == expected, f"Results in {results_file} do not match the expected output. Got: {lines}"

def test_property_tests_exist_and_pass():
    test_file = "/home/user/project/test_eval.py"
    assert os.path.isfile(test_file), f"Test file {test_file} is missing."

    with open(test_file, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "The test file does not import/use hypothesis."
    assert "given" in content, "The test file does not use hypothesis.given."
    assert "st.integers" in content or "strategies.integers" in content, "The test file does not use integer strategies."

    # Run the pytest file
    result = subprocess.run(
        ["pytest", test_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"pytest on {test_file} failed. Output:\n{result.stdout}\n{result.stderr}"