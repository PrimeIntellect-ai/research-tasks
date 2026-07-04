# test_final_state.py
import json
import os
import math

def test_profile_results_json():
    results_file = "/home/user/profile_results.json"
    assert os.path.exists(results_file), f"File {results_file} not found."

    with open(results_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_file} contains invalid JSON."

    required_keys = ["t_stat", "p_value", "wasserstein_dist"]
    for key in required_keys:
        assert key in data, f"Missing key '{key}' in {results_file}."
        assert isinstance(data[key], (float, int)), f"Key '{key}' must be a float."

    try:
        import numpy as np
        from scipy.integrate import solve_ivp
        from scipy.stats import wasserstein_distance

        def ode(t, y):
            r = 1.5
            K = 100.0
            return r * y * (1 - y / K)

        t_span = (0, 15)
        t_eval = np.linspace(0, 15, 300)
        y0 = [1.0]
        sol_rk45 = solve_ivp(ode, t_span, y0, method='RK45', t_eval=t_eval)
        sol_radau = solve_ivp(ode, t_span, y0, method='Radau', t_eval=t_eval)
        expected_wd = wasserstein_distance(sol_rk45.y[0], sol_radau.y[0])
    except ImportError:
        expected_wd = None

    if expected_wd is not None:
        assert math.isclose(data["wasserstein_dist"], expected_wd, abs_tol=1e-5), \
            f"Incorrect wasserstein_dist. Expected {expected_wd}, got {data['wasserstein_dist']}"