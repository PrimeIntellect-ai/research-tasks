# test_final_state.py

import os
import subprocess
import pytest

def test_integrate_script_fixed():
    script_path = "/home/user/integrate.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    # Test the script on a known file
    test_file = "/home/user/simulation_runs/run_1.csv"
    assert os.path.isfile(test_file), f"Missing {test_file}"

    result = subprocess.run([script_path, test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"integrate.sh failed with error: {result.stderr}"

    output = result.stdout.strip()
    try:
        val = float(output)
    except ValueError:
        pytest.fail(f"integrate.sh did not output a valid float: '{output}'")

    # The integral of 3*t^2 from 0 to 10 is 1000. With noise, it should be between 900 and 1100.
    assert 900 < val < 1100, f"integrate.sh output {val} is far from the expected ~1000. Trapezoidal rule might be incorrect."

def test_all_integrals_file():
    file_path = "/home/user/all_integrals.txt"
    assert os.path.isfile(file_path), f"Missing {file_path}"

    with open(file_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 50, f"Expected 50 lines in {file_path}, found {len(lines)}"

    for i, line in enumerate(lines):
        try:
            val = float(line)
            assert 800 < val < 1200, f"Value {val} on line {i+1} is out of expected range."
        except ValueError:
            pytest.fail(f"Invalid float '{line}' on line {i+1} in {file_path}")

def test_bootstrap_script_exists_and_executable():
    script_path = "/home/user/bootstrap.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_ci_file():
    file_path = "/home/user/ci.txt"
    assert os.path.isfile(file_path), f"Missing {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 2, f"Expected two comma-separated values in {file_path}, got '{content}'"

    try:
        low = float(parts[0])
        high = float(parts[1])
    except ValueError:
        pytest.fail(f"Could not parse floats from {file_path}: '{content}'")

    assert low < high, f"Lower bound {low} is not less than upper bound {high}"
    assert 900 < low < 1100, f"Lower bound {low} is out of expected range"
    assert 900 < high < 1100, f"Upper bound {high} is out of expected range"