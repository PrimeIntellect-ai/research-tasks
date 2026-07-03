# test_final_state.py

import os
import subprocess
import pytest

def test_venv_and_papermill():
    venv_papermill = "/home/user/venv/bin/papermill"
    assert os.path.isfile(venv_papermill), f"papermill executable not found at {venv_papermill}. Ensure the virtual environment is created and papermill is installed."

def test_run_analysis_script():
    script_path = "/home/user/run_analysis.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} is missing."

    # Execute the bash script to generate the outputs
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_analysis.sh failed to execute. stderr: {result.stderr}"

def test_notebook_output_exists():
    out_notebook = "/home/user/analysis_out.ipynb"
    assert os.path.isfile(out_notebook), f"Output notebook {out_notebook} was not created."

def test_ci_results():
    results_file = "/home/user/ci_results.txt"
    assert os.path.isfile(results_file), f"Results file {results_file} was not created."

    with open(results_file, "r") as f:
        content = f.read().strip()

    parts = content.split(",")
    assert len(parts) == 2, f"Expected two comma-separated values in {results_file}, got: {content}"

    try:
        lower_bound = float(parts[0])
        upper_bound = float(parts[1])
    except ValueError:
        pytest.fail(f"Could not parse floats from {results_file} content: {content}")

    # Recompute the expected values
    import numpy as np
    y0_vals = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    y5_vals = y0_vals / (2.5 * y0_vals + 1)

    np.random.seed(42)
    n_bootstrap = 5000
    means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(y5_vals, size=len(y5_vals), replace=True)
        means.append(np.mean(sample))

    expected_lower = np.percentile(means, 2.5)
    expected_upper = np.percentile(means, 97.5)

    # Check bounds with a small tolerance for formatting differences
    assert abs(lower_bound - expected_lower) < 1e-4, f"Lower bound {lower_bound} does not match expected {expected_lower}"
    assert abs(upper_bound - expected_upper) < 1e-4, f"Upper bound {upper_bound} does not match expected {expected_upper}"