# test_final_state.py

import os
import importlib.util

def test_setup_fixed():
    setup_path = '/home/user/fastsum_project/setup.py'
    assert os.path.isfile(setup_path), "setup.py is missing."
    with open(setup_path, 'r') as f:
        content = f.read()
    assert 'fastsum.c' in content, "setup.py was not fixed to use 'fastsum.c'."
    assert 'wrong_source.c' not in content, "setup.py still contains 'wrong_source.c'."

def test_fastsum_installed():
    try:
        import fastsum
    except ImportError:
        assert False, "The 'fastsum' package is not installed or importable."

    # Test if it actually works
    res = fastsum.solve([1, 2, 3], 3)
    assert res is not None, "fastsum.solve returned None unexpectedly."
    assert sum([1, 2, 3][i] for i in res) == 3, "fastsum.solve did not return correct indices."

def test_test_script_exists_and_valid():
    script_path = '/home/user/test_fastsum.py'
    assert os.path.isfile(script_path), f"Test script {script_path} is missing."
    with open(script_path, 'r') as f:
        content = f.read()

    assert 'test_subset_sum' in content, "The test function is not named 'test_subset_sum'."
    assert '@given' in content, "The test script does not use the @given decorator from hypothesis."
    assert 'hypothesis' in content, "The test script does not import hypothesis."
    assert 'fastsum' in content, "The test script does not import fastsum."

def test_test_results_exist_and_passed():
    results_path = '/home/user/test_results.txt'
    assert os.path.isfile(results_path), f"Test results file {results_path} is missing."
    with open(results_path, 'r') as f:
        content = f.read().lower()

    assert "passed" in content, "Pytest output does not indicate successful execution ('passed' not found)."
    assert "failed" not in content, "Pytest output indicates test failures."
    assert "error" not in content, "Pytest output indicates errors."