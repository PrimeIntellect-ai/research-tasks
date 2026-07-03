# test_final_state.py

import os

def test_solver_cpp_exists():
    """Check if the C++ source file was created."""
    assert os.path.exists('/home/user/solver.cpp'), "The file /home/user/solver.cpp does not exist."

def test_solver_so_exists():
    """Check if the shared library was compiled."""
    assert os.path.exists('/home/user/solver.so'), "The shared library /home/user/solver.so does not exist."

def test_fit_model_py_exists():
    """Check if the Python script was created."""
    assert os.path.exists('/home/user/fit_model.py'), "The file /home/user/fit_model.py does not exist."

def test_result_sse_content():
    """Check if the final SSE result is correct."""
    result_file = '/home/user/result_sse.txt'
    assert os.path.exists(result_file), f"The file {result_file} does not exist."

    with open(result_file, 'r') as f:
        content = f.read().strip()

    assert content == "0.0850", f"Expected SSE to be '0.0850', but got '{content}'."