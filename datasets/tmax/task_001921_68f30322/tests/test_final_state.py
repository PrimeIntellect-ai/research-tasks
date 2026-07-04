# test_final_state.py
import os
import subprocess
import re
import pytest

def test_analyze_core_script_exists():
    script_path = "/home/user/analyze_core.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_analyze_core_output_and_metrics():
    script_path = "/home/user/analyze_core.sh"

    try:
        result = subprocess.run([script_path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed with return code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    out = result.stdout

    match_mean = re.search(r'MEAN_MASS:\s*([0-9.]+)', out)
    assert match_mean is not None, f"MEAN_MASS not found in output:\n{out}"
    mass = float(match_mean.group(1))

    match_lower = re.search(r'CI_LOWER:\s*([0-9.]+)', out)
    assert match_lower is not None, f"CI_LOWER not found in output:\n{out}"
    ci_lower = float(match_lower.group(1))

    match_upper = re.search(r'CI_UPPER:\s*([0-9.]+)', out)
    assert match_upper is not None, f"CI_UPPER not found in output:\n{out}"
    ci_upper = float(match_upper.group(1))

    true_mass = 2955.62
    error = abs(mass - true_mass) / true_mass

    assert error <= 0.05, f"MEAN_MASS {mass} deviates more than 5% from truth {true_mass}. Error: {error:.4f}"

    assert ci_lower <= true_mass, f"CI_LOWER {ci_lower} should be <= true_mass {true_mass}"
    assert ci_upper >= true_mass, f"CI_UPPER {ci_upper} should be >= true_mass {true_mass}"