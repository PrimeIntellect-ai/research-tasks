# test_final_state.py

import os
import json
import subprocess

def test_model_fit_output():
    """
    Validates that the output JSON file exists, has the correct keys,
    and the values match the expected ground truth derived from the same
    deterministic procedure.
    """
    output_file = '/home/user/model_fit.json'
    assert os.path.isfile(output_file), f"The expected output file was not found at {output_file}."

    with open(output_file, 'r') as f:
        try:
            student_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {output_file} is not valid JSON."

    expected_keys = {"f0", "A_estimate", "A_ci_lower", "A_ci_upper"}
    actual_keys = set(student_data.keys())
    assert actual_keys == expected_keys, f"JSON keys mismatch. Expected {expected_keys}, found {actual_keys}."

    for key in expected_keys:
        assert isinstance(student_data[key], (int, float)), f"Value for '{key}' must be a float."

    # To compute the truth robustly without importing third-party libraries directly into the test process,
    # we can run a short Python script using the environment's installed libraries (numpy, scipy, pandas).
    truth_script = """
import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq
from scipy.optimize import root_scalar
import json

def estimate_A(y, N):
    yf = np.abs(fft(y))
    yf[0] = 0
    idx = np.argmax(yf[:N//2])
    P_max = yf[idx]
    C_est = P_max / (N / 2)
    def func(A):
        return A * np.exp(A) - C_est
    res = root_scalar(func, bracket=[0, 10])
    return idx, res.root

def main():
    df = pd.read_csv('/home/user/noisy_signal.csv')
    y = df['y'].values
    N = len(y)
    fs = 100.0

    idx, A_est = estimate_A(y, N)
    freqs = fftfreq(N, 1/fs)
    f0 = freqs[idx]

    A_sims = []
    for i in range(1000):
        rng = np.random.default_rng(42 + i)
        noise = rng.normal(loc=0.0, scale=0.5, size=N)
        y_noisy = y + noise
        _, A_sim = estimate_A(y_noisy, N)
        A_sims.append(A_sim)

    A_ci_lower = np.percentile(A_sims, 2.5)
    A_ci_upper = np.percentile(A_sims, 97.5)

    truth = {
        "f0": round(float(f0), 3),
        "A_estimate": round(float(A_est), 3),
        "A_ci_lower": round(float(A_ci_lower), 3),
        "A_ci_upper": round(float(A_ci_upper), 3)
    }
    print(json.dumps(truth))

if __name__ == '__main__':
    main()
"""
    script_path = '/tmp/compute_truth.py'
    with open(script_path, 'w') as f:
        f.write(truth_script)

    try:
        result = subprocess.run(['python3', script_path], capture_output=True, text=True, check=True)
        truth_data = json.loads(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        # Fallback to approximate checks if the script fails to run due to missing dependencies in the test env
        assert abs(student_data["f0"] - 3.0) < 0.1, "f0 is incorrect."
        assert 1.1 < student_data["A_estimate"] < 1.3, "A_estimate is out of expected bounds."
        assert student_data["A_ci_lower"] < student_data["A_estimate"] < student_data["A_ci_upper"], "Invalid confidence interval bounds."
        return
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)

    # Compare student data against computed truth
    for key in expected_keys:
        expected_val = truth_data[key]
        student_val = student_data[key]
        assert abs(student_val - expected_val) <= 0.001, (
            f"Value for '{key}' is incorrect. "
            f"Expected approximately {expected_val}, got {student_val}."
        )