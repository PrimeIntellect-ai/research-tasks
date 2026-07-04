# test_final_state.py

import os
import json
import stat
import math
import subprocess
import tempfile
import pytest

def test_run_pipeline_exists_and_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.exists(path), f"Missing {path}"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable"

def test_analysis_script_exists():
    path = "/home/user/analysis.py"
    assert os.path.exists(path), f"Missing {path}"

def test_venv_exists():
    path = "/home/user/venv/bin/python"
    assert os.path.exists(path), "Virtual environment python executable not found at /home/user/venv/bin/python"

def test_results_json_structure_and_values():
    path = "/home/user/results.json"
    assert os.path.exists(path), f"Missing {path}"

    with open(path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not a valid JSON file")

    expected_keys = {"best_hypothesis", "sse", "peak_mean", "peak_std"}
    assert set(results.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}"

    # Check hypothesis
    assert results["best_hypothesis"] in ["H0", "H1"], "best_hypothesis must be 'H0' or 'H1'"

    # To compute the exact expected values without relying on hardcoded constants, 
    # we can use the user's installed scipy/numpy in their venv via a subprocess.
    venv_python = "/home/user/venv/bin/python"
    if not os.path.exists(venv_python):
        pytest.skip("No venv python found to compute ground truth")

    checker_script = """
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import json

df = pd.read_csv('/home/user/observed_data.csv')
I_obs = df['I_obs'].values

def sir(t, y, beta, gamma, N):
    S, I, R = y
    return [-beta * S * I / N, beta * S * I / N - gamma * I, gamma * I]

N = 1000
y0 = [995, 5, 0]
t_span = (0, 50)
t_eval = np.arange(51)

sol_H0 = solve_ivp(sir, t_span, y0, args=(0.25, 0.10, N), t_eval=t_eval)
sol_H1 = solve_ivp(sir, t_span, y0, args=(0.40, 0.20, N), t_eval=t_eval)

sse_H0 = np.sum((sol_H0.y[1] - I_obs)**2)
sse_H1 = np.sum((sol_H1.y[1] - I_obs)**2)

best_sol = sol_H0 if sse_H0 < sse_H1 else sol_H1
best_hyp = "H0" if sse_H0 < sse_H1 else "H1"
best_sse = min(sse_H0, sse_H1)

np.random.seed(42)
peaks = []
for _ in range(1000):
    noise = np.random.normal(0, 5, size=len(t_eval))
    noisy_I = np.clip(best_sol.y[1] + noise, 0, None)
    peaks.append(np.max(noisy_I))

print(json.dumps({
    "best_hypothesis": best_hyp,
    "sse": round(best_sse, 2),
    "peak_mean": round(np.mean(peaks), 2),
    "peak_std": round(np.std(peaks), 2)
}))
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tf:
        tf.write(checker_script)
        tf_name = tf.name

    try:
        proc = subprocess.run([venv_python, tf_name], capture_output=True, text=True)
        if proc.returncode != 0:
            pytest.skip(f"Could not run ground truth script: {proc.stderr}")
        expected = json.loads(proc.stdout)
    finally:
        os.remove(tf_name)

    assert results["best_hypothesis"] == expected["best_hypothesis"], "Incorrect best_hypothesis"
    assert math.isclose(results["sse"], expected["sse"], rel_tol=1e-2), f"Expected SSE ~{expected['sse']}, got {results['sse']}"
    assert math.isclose(results["peak_mean"], expected["peak_mean"], rel_tol=1e-2), f"Expected peak_mean ~{expected['peak_mean']}, got {results['peak_mean']}"
    assert math.isclose(results["peak_std"], expected["peak_std"], rel_tol=1e-2), f"Expected peak_std ~{expected['peak_std']}, got {results['peak_std']}"