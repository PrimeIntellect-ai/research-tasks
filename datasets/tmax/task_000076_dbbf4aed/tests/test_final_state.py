# test_final_state.py

import os
import pytest

def test_evaluate_c_exists():
    """Test that evaluate.c exists."""
    file_path = "/home/user/pipeline/evaluate.c"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_libevaluate_so_exists():
    """Test that the compiled shared library libevaluate.so exists."""
    file_path = "/home/user/pipeline/libevaluate.so"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_solver_py_exists_and_uses_ctypes():
    """Test that solver.py exists and imports ctypes."""
    file_path = "/home/user/pipeline/solver.py"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "ctypes" in content, "solver.py does not appear to import or use ctypes."

def test_solution_txt_content():
    """Test that solution.txt contains the correct combination."""
    file_path = "/home/user/pipeline/solution.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content == "12,15,10,11", f"solution.txt contains '{content}', expected '12,15,10,11'."