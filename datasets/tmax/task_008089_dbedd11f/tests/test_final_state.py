# test_final_state.py
import os
import subprocess
import pytest

def compute_expected_iterations():
    nx, ny = 20, 20
    tol = 0.001
    max_iter = 5000

    grid = [0.0] * (nx * ny)
    for x in range(nx):
        grid[x] = 100.0

    next_grid = list(grid)

    iters = 0
    for _ in range(max_iter):
        max_error = 0.0
        for y in range(1, ny - 1):
            for x in range(1, nx - 1):
                val = 0.25 * (grid[(y-1)*nx + x] + grid[(y+1)*nx + x] + 
                              grid[y*nx + x - 1] + grid[y*nx + x + 1])
                next_grid[y*nx + x] = val

                err = abs(val - grid[y*nx + x])
                if err > max_error:
                    max_error = err

        for i in range(nx * ny):
            grid[i] = next_grid[i]

        iters += 1
        if max_error < tol:
            break

    return iters

def test_grid_config_restored():
    config_path = "/home/user/heat_solver/grid_config.txt"
    assert os.path.isfile(config_path), f"{config_path} is missing. Did you restore it from git history?"

    with open(config_path, "r") as f:
        content = f.read()

    assert "nx=20" in content, "grid_config.txt is missing expected nx=20 configuration"
    assert "ny=20" in content, "grid_config.txt is missing expected ny=20 configuration"
    assert "tol=0.001" in content, "grid_config.txt is missing expected tol=0.001 configuration"
    assert "max_iter=5000" in content, "grid_config.txt is missing expected max_iter=5000 configuration"

def test_makefile_fixed_and_executable_built():
    makefile_path = "/home/user/heat_solver/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing."

    # We test if the project can be built and run.
    # The executable should be built.
    executable_path = "/home/user/heat_solver/heat_sim"

    # If it's not there, try running make
    if not os.path.isfile(executable_path):
        result = subprocess.run(["make", "-C", "/home/user/heat_solver"], capture_output=True, text=True)
        assert result.returncode == 0, f"make failed to build the executable. Output: {result.stderr}"

    assert os.path.isfile(executable_path), f"{executable_path} was not built."

    # Run it to see if it works
    result = subprocess.run([executable_path], cwd="/home/user/heat_solver", capture_output=True, text=True)
    assert result.returncode == 0, f"Running {executable_path} failed. Output: {result.stderr}"
    assert "Converged in" in result.stdout, "Executable output did not contain 'Converged in'."

def test_result_file_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"{result_path} is missing. Did you write the final number of iterations to it?"

    with open(result_path, "r") as f:
        result_content = f.read().strip()

    expected_iters = compute_expected_iterations()

    assert str(expected_iters) in result_content, f"Expected {expected_iters} to be in {result_path}, but found '{result_content}'."