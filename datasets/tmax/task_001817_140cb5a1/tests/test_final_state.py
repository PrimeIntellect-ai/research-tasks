# test_final_state.py
import os
import json
import subprocess
import numpy as np
import pandas as pd

def test_script_execution_and_results():
    script_path = "/home/user/analyze_dynamics.sh"
    results_path = "/home/user/results.json"
    laplacian_path = "/app/laplacian.csv"

    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_path} is not valid JSON"

    required_keys = ["dominant_frequency_hz", "ci_95_lower", "ci_95_upper", "regularized_inverse_trace"]
    for key in required_keys:
        assert key in results, f"Missing key '{key}' in results.json"

    # Check dominant frequency
    freq = float(results["dominant_frequency_hz"])
    assert abs(freq - 4.5) <= 0.2, f"dominant_frequency_hz {freq} is not within 0.2 of 4.5"

    # Check CI bounds
    ci_lower = float(results["ci_95_lower"])
    assert abs(ci_lower - 4.4) <= 0.3, f"ci_95_lower {ci_lower} is not within 0.3 of 4.4"

    ci_upper = float(results["ci_95_upper"])
    assert abs(ci_upper - 4.6) <= 0.3, f"ci_95_upper {ci_upper} is not within 0.3 of 4.6"

    # Compute expected trace
    assert os.path.isfile(laplacian_path), f"Laplacian file not found at {laplacian_path}"
    L_df = pd.read_csv(laplacian_path, header=None)
    L = L_df.values
    L_reg = L + 0.01 * np.eye(L.shape[0])
    L_inv = np.linalg.inv(L_reg)
    expected_trace = np.trace(L_inv)

    trace_val = float(results["regularized_inverse_trace"])
    assert abs(trace_val - expected_trace) <= 0.05, f"regularized_inverse_trace {trace_val} is not within 0.05 of expected {expected_trace}"