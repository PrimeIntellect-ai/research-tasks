# test_final_state.py

import os
import pytest

def test_makefile_fixed():
    makefile_path = "/home/user/math_project/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-lm" in content, "Makefile does not contain the '-lm' linker flag required to fix the build."

def test_math_app_compiled():
    app_path = "/home/user/math_project/math_app"
    assert os.path.isfile(app_path), f"Executable is missing at {app_path}. Did the build succeed?"
    assert os.access(app_path, os.X_OK), f"File at {app_path} is not executable."

def test_results_txt():
    results_path = "/home/user/math_project/results.txt"
    assert os.path.isfile(results_path), f"Results file is missing at {results_path}. Did you run the application?"

    expected_results = [
        60,
        2000000,
        26929944384,
        12000000000
    ]

    with open(results_path, "r") as f:
        lines = f.read().strip().splitlines()

    actual_results = []
    for line in lines:
        try:
            actual_results.append(int(line.strip()))
        except ValueError:
            pytest.fail(f"Found non-integer value in results.txt: '{line}'")

    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} results, but found {len(actual_results)}."

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        assert actual == expected, f"Result at line {i+1} is incorrect. Expected {expected}, got {actual}. The overflow bug might not be properly fixed."