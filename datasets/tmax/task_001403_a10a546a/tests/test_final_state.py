# test_final_state.py

import os
import math
import pytest

def test_venv_exists():
    """Verify that the virtual environment was created at the correct path."""
    venv_path = "/home/user/simulation/venv"
    assert os.path.isdir(venv_path), f"Virtual environment directory not found at {venv_path}"
    python_bin = os.path.join(venv_path, "bin", "python")
    assert os.path.isfile(python_bin) or os.path.isfile(os.path.join(venv_path, "Scripts", "python.exe")), "Python executable not found in virtual environment"

def test_script_modified():
    """Verify that the script was modified to use a least squares solver instead of solve."""
    script_path = "/home/user/simulation/poisson_matrix.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    assert "np.linalg.solve(" not in content, "The script still contains np.linalg.solve"
    assert "lstsq(" in content, "The script does not appear to use a least-squares solver (e.g., lstsq)"

def test_solution_max_file():
    """Verify that the solution_max.txt file exists and contains the correct scalar value."""
    file_path = "/home/user/simulation/solution_max.txt"
    assert os.path.isfile(file_path), f"Output file not found at {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content, "The solution_max.txt file is empty"

    try:
        max_val = float(content)
    except ValueError:
        pytest.fail(f"The content of solution_max.txt is not a valid float: '{content}'")

    expected_val = 1.25
    assert math.isclose(max_val, expected_val, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected value close to {expected_val}, but got {max_val}"