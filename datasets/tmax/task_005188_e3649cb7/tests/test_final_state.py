# test_final_state.py

import os
import re

def test_venv_exists():
    venv_path = "/home/user/venv"
    assert os.path.isdir(venv_path), f"Virtual environment directory not found at {venv_path}"
    python_bin = os.path.join(venv_path, "bin", "python")
    assert os.path.isfile(python_bin), f"Python executable not found in venv at {python_bin}"

def test_script_fixed():
    script_path = "/home/user/scripts/analyze.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    assert "np.linalg.inv" not in content, "The buggy OLS implementation (np.linalg.inv) was not removed."
    assert "Ridge" in content, "Ridge regression from scikit-learn was not found in the script."
    assert "alpha=1.0" in content.replace(" ", ""), "Ridge regression must be initialized with alpha=1.0."
    assert "fit_intercept=False" in content.replace(" ", ""), "Ridge regression must be initialized with fit_intercept=False."

def test_results_file_and_values():
    results_path = "/home/user/results/coefficients.txt"
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 coefficients in the results file, found {len(lines)}"

    try:
        coeffs = [float(line) for line in lines]
    except ValueError:
        assert False, "Results file contains non-numeric values."

    expected_coeffs = [0.2117, 0.0195, 0.0389]

    for i, (actual, expected) in enumerate(zip(coeffs, expected_coeffs)):
        assert abs(actual - expected) < 0.001, f"Coefficient {i+1} is incorrect. Expected ~{expected}, got {actual}"