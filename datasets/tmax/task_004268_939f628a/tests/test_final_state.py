# test_final_state.py
import pytest
import requests
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import brentq

def fun(t, state):
    x, y, vx, vy = state
    return np.array([vx, vy, -x - 0.5 * x**3, -y - 0.5 * y**3])

def solve_ivp_adaptive_ref(fun, t_span, y0, tol=1e-6, dt_init=0.01):
    t_start, t_end = t_span
    t = [t_start]
    y = [np.array(y0)]
    dt = dt_init

    t_curr = t_start
    y_curr = np.array(y0)

    while t_curr < t_end:
        if t_curr + dt > t_end:
            dt = t_end - t_curr

        k1 = fun(t_curr, y_curr)
        k2 = fun(t_curr + dt, y_curr + dt * k1)

        y_next = y_curr + dt * 0.5 * (k1 + k2)
        y_euler = y_curr + dt * k1

        error = np.max(np.abs(y_next - y_euler)) + 1e-12

        if error < tol:
            t_curr += dt
            y_curr = y_next
            t.append(t_curr)
            y.append(y_curr)

        dt = dt * (tol / error)**0.2 
        dt = np.clip(dt, 1e-6, 0.5)

    return np.array(t), np.array(y)

def compute_reference_values():
    y0 = np.array([1.0, 1.0, 0.0, 0.0], dtype=np.float64)
    np.random.seed(42)
    perturbed_states = y0 + np.random.normal(0, 0.01, (100, 4))

    crossing_times = []
    for state in perturbed_states:
        t_arr, y_arr = solve_ivp_adaptive_ref(fun, (0, 10), state)
        y_vals = y_arr[:, 1]
        vy_vals = y_arr[:, 3]

        for i in range(len(t_arr)-1):
            if y_vals[i] > 0 and y_vals[i+1] <= 0:
                # Crossed 0 from positive to negative
                # Use cubic interpolation if possible, otherwise linear
                start_idx = max(0, i-1)
                end_idx = min(len(t_arr), i+3)

                t_sub = t_arr[start_idx:end_idx]
                y_sub = y_vals[start_idx:end_idx]

                kind = 'cubic' if len(t_sub) >= 4 else 'linear'
                f_interp = interp1d(t_sub, y_sub, kind=kind)

                try:
                    t_cross = brentq(f_interp, t_arr[i], t_arr[i+1])
                    crossing_times.append(t_cross)
                except ValueError:
                    # Fallback to linear
                    f_interp_lin = interp1d(t_arr[i:i+2], y_vals[i:i+2], kind='linear')
                    t_cross = brentq(f_interp_lin, t_arr[i], t_arr[i+1])
                    crossing_times.append(t_cross)
                break

    crossing_times = np.array(crossing_times)

    np.random.seed(42)
    boot_means = []
    for _ in range(1000):
        sample = np.random.choice(crossing_times, size=len(crossing_times), replace=True)
        boot_means.append(np.mean(sample))

    t_crossing_mean = np.mean(crossing_times)
    ci_95_lower = np.percentile(boot_means, 2.5)
    ci_95_upper = np.percentile(boot_means, 97.5)

    return t_crossing_mean, ci_95_lower, ci_95_upper

def test_metrics_endpoint():
    url = "http://127.0.0.1:8080/metrics"

    # 1. Without auth header -> 401
    resp_no_auth = requests.get(url)
    assert resp_no_auth.status_code == 401, f"Expected 401 Unauthorized without auth header, got {resp_no_auth.status_code}"

    # 2. With wrong auth header -> 401
    resp_wrong_auth = requests.get(url, headers={"X-Auth-Token": "wrong-secret"})
    assert resp_wrong_auth.status_code == 401, f"Expected 401 Unauthorized with wrong auth header, got {resp_wrong_auth.status_code}"

    # 3. With correct auth header -> 200
    resp_auth = requests.get(url, headers={"X-Auth-Token": "perf-eng-secret"})
    assert resp_auth.status_code == 200, f"Expected 200 OK with correct auth header, got {resp_auth.status_code}"

    data = resp_auth.json()
    assert "t_crossing_mean" in data, "Response missing 't_crossing_mean'"
    assert "ci_95_lower" in data, "Response missing 'ci_95_lower'"
    assert "ci_95_upper" in data, "Response missing 'ci_95_upper'"

    # 4. Check values
    ref_mean, ref_lower, ref_upper = compute_reference_values()

    # We allow a generous tolerance due to potential differences in interpolation methods (linear vs cubic vs spline)
    tol = 0.05
    assert abs(data["t_crossing_mean"] - ref_mean) < tol, f"t_crossing_mean {data['t_crossing_mean']} is not close to reference {ref_mean}"
    assert abs(data["ci_95_lower"] - ref_lower) < tol, f"ci_95_lower {data['ci_95_lower']} is not close to reference {ref_lower}"
    assert abs(data["ci_95_upper"] - ref_upper) < tol, f"ci_95_upper {data['ci_95_upper']} is not close to reference {ref_upper}"

def test_scipack_fix():
    with open("/app/scipack-1.0.0/scipack/ode.py", "r") as f:
        content = f.read()
    assert "dt = dt * (tol / error)" in content or "dt = dt * (error / tol)**(-0.2)" in content or "dt *= (tol / error)" in content, "The adaptive step size bug in scipack/ode.py does not appear to be fixed."