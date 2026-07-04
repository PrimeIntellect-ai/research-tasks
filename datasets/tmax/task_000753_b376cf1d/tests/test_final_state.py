# test_final_state.py
import os
import json
import subprocess
import pytest

def test_sim_env_exists():
    """Verify that the Python virtual environment was created."""
    venv_python = '/home/user/sim_env/bin/python'
    assert os.path.exists(venv_python), f"Virtual environment python not found at {venv_python}. Make sure you created it."

def test_results_json_structure_and_values():
    """Verify that results.json exists, has the correct keys, and correct values."""
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), f"The output file {results_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            student_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {results_path} is not valid JSON.")

    expected_keys = {"wasserstein_distance", "ci_lower", "ci_upper"}
    assert set(student_results.keys()) == expected_keys, f"Keys in results.json must be exactly {expected_keys}"

    for key in expected_keys:
        assert isinstance(student_results[key], (int, float)), f"Value for {key} must be a number."

    # Recompute the expected values using the student's virtual environment
    # to avoid importing numpy/scipy in the test environment directly.
    script = '''
import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import wasserstein_distance
import json

def epidemic_model(t, y, beta, gamma):
    S, I = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    return [dSdt, dIdt]

gamma = 0.15
y0 = [99.0, 1.0]
t_span = (0, 50)
t_eval = np.linspace(0, 50, 100)

np.random.seed(42)
beta_group1 = np.random.normal(0.30, 0.02, 500)
beta_group2 = np.random.normal(0.28, 0.02, 500)

D1 = []
for beta in beta_group1:
    sol = solve_ivp(epidemic_model, t_span, y0, args=(beta, gamma), t_eval=t_eval)
    D1.append(np.max(sol.y[1]))
D1 = np.array(D1)

D2 = []
for beta in beta_group2:
    sol = solve_ivp(epidemic_model, t_span, y0, args=(beta, gamma), t_eval=t_eval)
    D2.append(np.max(sol.y[1]))
D2 = np.array(D2)

w_dist = wasserstein_distance(D1, D2)

np.random.seed(100)
boot_dists = []
for _ in range(1000):
    idx1 = np.random.choice(len(D1), len(D1), replace=True)
    idx2 = np.random.choice(len(D2), len(D2), replace=True)
    b_D1 = D1[idx1]
    b_D2 = D2[idx2]
    boot_dists.append(wasserstein_distance(b_D1, b_D2))

ci_lower = np.percentile(boot_dists, 2.5)
ci_upper = np.percentile(boot_dists, 97.5)

print(json.dumps({
    "wasserstein_distance": round(float(w_dist), 4),
    "ci_lower": round(float(ci_lower), 4),
    "ci_upper": round(float(ci_upper), 4)
}))
'''
    env_python = '/home/user/sim_env/bin/python'
    try:
        proc = subprocess.run([env_python, '-c', script], capture_output=True, text=True, check=True)
        expected_results = json.loads(proc.stdout)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected results using the virtual environment. Ensure numpy and scipy are installed correctly: {e.stderr}")

    for key in expected_keys:
        expected_val = expected_results[key]
        student_val = student_results[key]
        assert abs(student_val - expected_val) <= 0.0001, f"Value for '{key}' is incorrect. Expected {expected_val}, got {student_val}."