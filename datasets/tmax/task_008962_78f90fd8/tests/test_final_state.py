# test_final_state.py

import os
import subprocess
import pytest

def test_solution_txt_correct():
    path = "/home/user/solution.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "0.0067", f"Expected '0.0067' in {path}, but got '{content}'."

def test_regression_sh_exists_and_passes():
    path = "/home/user/regression.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    # Run the regression script
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"{path} did not exit with code 0. Exit code: {result.returncode}, Output: {result.stdout} {result.stderr}"

def test_calc_variance_sh_stable():
    path = "/home/user/calc_variance.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    # Test it with large numbers that cause catastrophic cancellation in naive algorithms
    input_data = "100000000.1\n100000000.2\n100000000.3\n"
    result = subprocess.run([path], input=input_data, capture_output=True, text=True)

    assert result.returncode == 0, f"{path} failed to run."
    output = result.stdout.strip()
    assert output == "0.0067", f"Expected '0.0067' from {path}, but got '{output}'."