# test_final_state.py

import os
import subprocess
import pstats
import pytest

SIM_PROJECT_DIR = "/home/user/sim_project"

def test_libkernel_so_exists():
    so_path = os.path.join(SIM_PROJECT_DIR, "libkernel.so")
    assert os.path.isfile(so_path), f"{so_path} does not exist. Did you compile the C kernel?"

def test_fast_solver_py():
    py_path = os.path.join(SIM_PROJECT_DIR, "fast_solver.py")
    assert os.path.isfile(py_path), f"{py_path} does not exist."
    with open(py_path, "r") as f:
        content = f.read()

    assert "def parallel_solve" in content, "parallel_solve function not found in fast_solver.py"
    assert "ctypes" in content, "ctypes module not imported/used in fast_solver.py"
    assert "multiprocessing" in content or "concurrent.futures" in content, "multiprocessing or concurrent.futures not used in fast_solver.py"

def test_regression_tests_pass():
    test_file = os.path.join(SIM_PROJECT_DIR, "test_regression.py")
    assert os.path.isfile(test_file), f"{test_file} is missing."

    # Run pytest on the regression test
    result = subprocess.run(
        ["pytest", test_file],
        capture_output=True,
        text=True,
        cwd=SIM_PROJECT_DIR
    )
    assert result.returncode == 0, f"Regression tests failed. Pytest output:\n{result.stdout}\n{result.stderr}"

def test_run_profile_py_exists():
    py_path = os.path.join(SIM_PROJECT_DIR, "run_profile.py")
    assert os.path.isfile(py_path), f"{py_path} does not exist."

def test_profile_data_prof_exists_and_valid():
    prof_path = os.path.join(SIM_PROJECT_DIR, "profile_data.prof")
    assert os.path.isfile(prof_path), f"{prof_path} does not exist. Did you run cProfile and output to this file?"

    try:
        stats = pstats.Stats(prof_path)
        assert len(stats.stats) > 0, "Profile data appears empty."
    except Exception as e:
        pytest.fail(f"Failed to load {prof_path} as a valid cProfile output: {e}")