# test_final_state.py

import os
import subprocess
import math

def test_final_protein_txt():
    path = "/home/user/final_protein.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you write the final protein concentration?"

    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} is not a valid float: '{content}'")

    # Expected analytical value is ~0.3161
    expected = 0.3161
    assert math.isclose(val, expected, abs_tol=0.005), f"Expected final protein concentration close to {expected}, but got {val}"

def test_protein_plot_exists():
    path = "/home/user/protein_plot.png"
    assert os.path.isfile(path), f"File {path} is missing. Did you save the plot?"
    assert os.path.getsize(path) > 0, f"File {path} is empty."

def test_pytest_simulate_passes():
    path = "/home/user/test_simulate.py"
    assert os.path.isfile(path), f"Test file {path} is missing."

    # Run pytest on the student's test file
    result = subprocess.run(
        ["pytest", path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"pytest on {path} failed. Output:\n{result.stdout}\n{result.stderr}"

def test_simulate_uses_solve_ivp():
    path = "/home/user/simulate.py"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    assert "solve_ivp" in content, "The script does not seem to use scipy.integrate.solve_ivp as requested."
    assert "BDF" in content or "Radau" in content or "LSODA" in content, "The script does not seem to specify a stiff solver (e.g., BDF, Radau, LSODA)."