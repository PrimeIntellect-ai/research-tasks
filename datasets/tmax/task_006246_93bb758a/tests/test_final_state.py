# test_final_state.py

import os
import pytest

def test_solution_file_content():
    solution_path = "/home/user/stiff_ode/solution.txt"
    assert os.path.isfile(solution_path), f"File {solution_path} is missing. The Rust program must create it."

    with open(solution_path, "r") as f:
        content = f.read().strip()

    expected = "0.5000,-0.5000,-0.5000,0.5000"
    assert content == expected, f"Content of {solution_path} is incorrect. Expected '{expected}', got '{content}'."

def test_main_rs_modifications():
    main_rs_path = "/home/user/stiff_ode/src/main.rs"
    assert os.path.isfile(main_rs_path), f"File {main_rs_path} is missing."

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "a.solve(&b)" not in content, "The buggy LU solve `a.solve(&b)` should be removed from main.rs."
    assert "svd" in content.lower(), "The code should compute the SVD of the matrix."