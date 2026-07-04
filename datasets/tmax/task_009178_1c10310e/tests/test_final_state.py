# test_final_state.py

import os
import glob
import pytest

def test_adler32_c_fixed():
    c_file = "/home/user/project/adler32.c"
    assert os.path.isfile(c_file), f"File {c_file} does not exist."

    with open(c_file, "r") as f:
        content = f.read()

    assert "65521" in content, "The C file was not fixed to use the correct MOD_ADLER value (65521)."
    assert "65536" not in content, "The C file still contains the buggy MOD_ADLER value (65536)."

def test_setup_py_fixed():
    setup_file = "/home/user/project/setup.py"
    assert os.path.isfile(setup_file), f"File {setup_file} does not exist."

    with open(setup_file, "r") as f:
        content = f.read()

    assert "adler32.c" in content, "The setup.py file was not fixed to reference 'adler32.c'."
    assert "wrong_file.c" not in content, "The setup.py file still references 'wrong_file.c'."

def test_module_built():
    # Check if the shared object file was built in-place
    so_files = glob.glob("/home/user/project/adler32_fast*.so")
    assert len(so_files) > 0, "The adler32_fast module was not built in-place."

def test_compare_sh_exists_and_executable():
    script_file = "/home/user/project/compare.sh"
    assert os.path.isfile(script_file), f"Script {script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"Script {script_file} is not executable."

def test_comparison_results():
    results_file = "/home/user/project/comparison_results.txt"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

    with open(results_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "file1.txt: MATCH",
        "file2.txt: MISMATCH",
        "file3.txt: MATCH"
    ]

    assert lines == expected_lines, (
        f"The contents of {results_file} do not match the expected sorted output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {lines}"
    )