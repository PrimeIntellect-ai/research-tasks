# test_final_state.py
import os
import math
import subprocess
import pytest

def test_final_loss_file():
    path = "/home/user/final_loss.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the executable?"

    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        loss = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} is not a valid float: '{content}'")

    assert not math.isnan(loss), "Final loss is NaN, indicating exploding gradients. Regularization may be missing or incorrect."
    assert loss < 50000, f"Final loss {loss} is too high. Regularization may be incorrectly implemented."

def test_mf_cpp_openmp_pragmas():
    path = "/home/user/mf.cpp"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "#pragma omp parallel for" in content, "OpenMP pragma '#pragma omp parallel for' not found in mf.cpp."

def test_executable_compiled_with_openmp():
    path = "/home/user/mf"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile the code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    result = subprocess.run(["ldd", path], capture_output=True, text=True)
    assert "omp" in result.stdout.lower(), "Executable does not seem to be linked with OpenMP (libgomp/libomp not found in ldd output). Did you compile with -fopenmp?"