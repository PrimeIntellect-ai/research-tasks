# test_final_state.py
import os
import re
import subprocess
import pytest

def test_solver_c_exists():
    """Check if the C solver source file exists."""
    assert os.path.isfile("/home/user/solver.c"), "/home/user/solver.c does not exist."

def test_orchestrate_sh_exists_and_executable():
    """Check if the orchestration script exists and is executable."""
    script_path = "/home/user/orchestrate.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_orchestrate_sh_execution():
    """Run the orchestration script and ensure it succeeds."""
    script_path = "/home/user/orchestrate.sh"
    # Execute the script in the user's home directory
    result = subprocess.run([script_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, (
        f"orchestrate.sh failed with return code {result.returncode}.\n"
        f"Stdout:\n{result.stdout}\n"
        f"Stderr:\n{result.stderr}"
    )

def test_ci_results():
    """Check if ci_results.txt is generated correctly and values are within expected bounds."""
    results_path = "/home/user/ci_results.txt"
    assert os.path.isfile(results_path), f"{results_path} does not exist. The script failed to create it."

    with open(results_path, "r") as f:
        content = f.read()

    lower_match = re.search(r"Lower CI:\s*([\d.]+)", content)
    upper_match = re.search(r"Upper CI:\s*([\d.]+)", content)

    assert lower_match is not None, f"Could not find 'Lower CI: <value>' in {results_path}. Content:\n{content}"
    assert upper_match is not None, f"Could not find 'Upper CI: <value>' in {results_path}. Content:\n{content}"

    try:
        lower_ci = float(lower_match.group(1))
        upper_ci = float(upper_match.group(1))
    except ValueError:
        pytest.fail("Parsed CI values are not valid floats.")

    # Check if the confidence intervals fall within the expected stochastic ranges
    assert 1.9000 <= lower_ci <= 1.9500, f"Lower CI {lower_ci} is out of the expected range [1.9000, 1.9500]"
    assert 2.0200 <= upper_ci <= 2.0700, f"Upper CI {upper_ci} is out of the expected range [2.0200, 2.0700]"