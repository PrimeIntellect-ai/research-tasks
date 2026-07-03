# test_final_state.py

import os
import re
import math
import pytest

def test_bad_commit_hash():
    bad_commit_file = "/home/user/bad_commit.txt"
    expected_commit_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(bad_commit_file), f"File {bad_commit_file} does not exist. You must create it."
    assert os.path.isfile(expected_commit_file), f"Truth file {expected_commit_file} is missing."

    with open(bad_commit_file, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_commit_file, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The commit hash in {bad_commit_file} is incorrect. Expected {expected_hash}, got {actual_hash}."

def test_solution_file():
    solution_file = "/home/user/solution.txt"
    assert os.path.isfile(solution_file), f"File {solution_file} does not exist. You must create it."

    with open(solution_file, "r") as f:
        content = f.read().strip()

    # The format should be X.XXXX, Y.XXXX
    match = re.match(r"^([0-9\.\-]+)\s*,\s*([0-9\.\-]+)$", content)
    assert match, f"The format of {solution_file} is incorrect. It should be 'X.XXXX, Y.XXXX'."

    x, y = float(match.group(1)), float(match.group(2))

    # Expected approximate geometric median for (0,0), (0,4), (3,0)
    expected_x = 0.85865
    expected_y = 1.14487

    assert math.isclose(x, expected_x, abs_tol=0.001), f"The X coordinate {x} is incorrect. It should be approximately 0.8587."
    assert math.isclose(y, expected_y, abs_tol=0.001), f"The Y coordinate {y} is incorrect. It should be approximately 1.1449."

def test_solver_script_fixed():
    import sys
    repo_dir = "/home/user/weiszfeld_solver"
    sys.path.insert(0, repo_dir)

    try:
        import solver
    except ImportError:
        pytest.fail(f"Could not import solver.py from {repo_dir}.")

    assert hasattr(solver, "solve"), "solver.py is missing the 'solve' function."

    points = [(0.0, 0.0), (0.0, 4.0), (3.0, 0.0)]
    initial_guess = (0.0, 0.0)

    try:
        result = solver.solve(points, initial_guess, iterations=100)
    except ZeroDivisionError:
        pytest.fail("The solver still raises ZeroDivisionError when the guess coincides with a point.")
    except Exception as e:
        pytest.fail(f"The solver raised an unexpected error: {e}")

    assert len(result) == 2, "The solve function should return a tuple of (X, Y)."
    assert not math.isnan(result[0]) and not math.isnan(result[1]), "The solver returned NaN."