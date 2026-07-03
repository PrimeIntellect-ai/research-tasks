# test_final_state.py

import os
import re
import pytest

def test_solution_txt():
    path = "/home/user/pr_review/solution.txt"
    assert os.path.isfile(path), f"{path} does not exist. Did you run the program and redirect output?"

    with open(path, "r") as f:
        content = f.read().strip()

    lines = content.split('\n')
    assert len(lines) == 3, f"solution.txt must contain exactly 3 lines, found {len(lines)}"

    grid = []
    for line in lines:
        parts = line.strip().split()
        assert len(parts) == 3, f"Each line must contain exactly 3 numbers, got: '{line}'"
        try:
            grid.append([int(p) for p in parts])
        except ValueError:
            pytest.fail(f"Could not parse integers from line: '{line}'")

    # Check if it's a valid magic square
    used = set()
    for row in grid:
        for val in row:
            assert 1 <= val <= 9, f"Value {val} out of range 1-9"
            used.add(val)
    assert len(used) == 9, "Grid must contain all numbers 1-9 exactly once"

    # Check sums
    for i in range(3):
        assert sum(grid[i]) == 15, f"Row {i} does not sum to 15"
        assert sum(grid[r][i] for r in range(3)) == 15, f"Column {i} does not sum to 15"

    assert grid[0][0] + grid[1][1] + grid[2][2] == 15, "Main diagonal does not sum to 15"
    assert grid[0][2] + grid[1][1] + grid[2][0] == 15, "Anti-diagonal does not sum to 15"

    # Specific expected square (first one found by standard backtracking order 1-9)
    expected = [
        [2, 7, 6],
        [9, 5, 1],
        [4, 3, 8]
    ]
    assert grid == expected, f"Expected the first valid magic square {expected}, but got {grid}"

def test_executable_exists():
    path = "/home/user/pr_review/magic_square"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you run make?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_makefile_fixed():
    path = "/home/user/pr_review/Makefile"
    assert os.path.isfile(path), f"Makefile {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "fast_sum" in content, "Makefile does not appear to include fast_sum.s in the build."

def test_cpp_fixed():
    path = "/home/user/pr_review/magic_square.cpp"
    assert os.path.isfile(path), f"Source file {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # The anti-diagonal check must be present.
    # Check if grid[0][2] or grid[2][0] is used in a fast_sum call.
    has_anti_diag = re.search(r'fast_sum\s*\([^)]*grid\[0\]\[2\]', content) or \
                    re.search(r'fast_sum\s*\([^)]*grid\[2\]\[0\]', content)

    assert has_anti_diag, "magic_square.cpp does not appear to contain the anti-diagonal check using fast_sum."