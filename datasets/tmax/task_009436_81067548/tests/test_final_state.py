# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/matrix_profiler"

def test_matrix_c_recovered_and_fixed():
    matrix_c = os.path.join(WORKSPACE_DIR, "matrix.c")
    assert os.path.isfile(matrix_c), f"File {matrix_c} was not recovered."

    with open(matrix_c, "r") as f:
        content = f.read()

    # Check that the off-by-one error is fixed
    assert "i <= 5" not in content, "The off-by-one bug (i <= 5) in matrix.c was not fixed."
    assert "i < 5" in content or "i<=4" in content.replace(" ", ""), "The loop in matrix.c does not seem to be properly fixed."

def test_bt_txt_exists_and_valid():
    bt_txt = os.path.join(WORKSPACE_DIR, "bt.txt")
    assert os.path.isfile(bt_txt), f"File {bt_txt} was not created."

    with open(bt_txt, "r") as f:
        content = f.read()

    assert "compute_matrix" in content or "main" in content, "bt.txt does not contain a valid backtrace (missing 'compute_matrix' or 'main')."

def test_makefile_fixed_and_compiles():
    makefile = os.path.join(WORKSPACE_DIR, "Makefile")
    assert os.path.isfile(makefile), f"Makefile is missing."

    # Run make
    result = subprocess.run(["make"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with output:\n{result.stderr}\n{result.stdout}"

    app_fixed = os.path.join(WORKSPACE_DIR, "app_fixed")
    assert os.path.isfile(app_fixed), "make succeeded but app_fixed was not created."
    assert os.access(app_fixed, os.X_OK), "app_fixed is not executable."

def test_run_tests_sh():
    run_tests_sh = os.path.join(WORKSPACE_DIR, "run_tests.sh")
    assert os.path.isfile(run_tests_sh), f"File {run_tests_sh} is missing."
    assert os.access(run_tests_sh, os.X_OK), f"File {run_tests_sh} is not executable."

    # Remove test_results.log if it exists to ensure the script creates it
    log_file = os.path.join(WORKSPACE_DIR, "test_results.log")
    if os.path.exists(log_file):
        os.remove(log_file)

    result = subprocess.run(["./run_tests.sh"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"run_tests.sh failed with output:\n{result.stderr}\n{result.stdout}"

    assert os.path.isfile(log_file), f"{log_file} was not created by run_tests.sh."

    with open(log_file, "r") as f:
        content = f.read()

    assert "ALL TESTS PASSED" in content, f"{log_file} does not contain 'ALL TESTS PASSED'."