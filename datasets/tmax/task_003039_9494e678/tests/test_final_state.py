# test_final_state.py
import os
import math

def test_integrator_c_fixed():
    path = "/home/user/integrator.c"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "tol / error" in content, "The logic bug was not fixed. Expected 'tol / error' in step_update."
    assert "error / tol" not in content, "The buggy logic 'error / tol' is still present in the file."

def test_executable_exists():
    path = "/home/user/integrator"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_output_bin_exists():
    path = "/home/user/output.bin"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the executable?"
    assert os.path.getsize(path) > 0, f"File {path} is empty."

def test_final_distance():
    path = "/home/user/final_distance.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    # Compute expected distance
    x, y = 1.0, 0.0
    h = 0.1
    tol = 1e-6

    for _ in range(1000):
        error = h * h * 0.5
        if error <= 0: 
            error = 1e-15
        h = h * 0.9 * ((tol / error) ** 0.2)
        x += y * h
        y -= x * h

    expected_distance = math.sqrt(x*x + y*y)
    expected_str = f"{expected_distance:.4f}"

    with open(path, "r") as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected distance {expected_str}, but got {actual_str} in {path}."