# test_final_state.py
import os
import math
import pytest

# Although the prompt says "no third-party libs", numpy and scipy are explicitly
# part of the system environment for this task. However, to strictly adhere to the 
# "only Python standard library" rule for the test suite, we can implement the 
# required logic in pure Python, optimizing the search to avoid timeouts.

def vdp_deriv(t, y, mu):
    return [y[1], mu * (1.0 - y[0]**2) * y[1] - y[0]]

def adaptive_euler_heun_fixed(mu, t_end=600.0, dt0=0.1, tol=1e-3):
    t = 0.0
    y = [2.0, 0.0]
    times = [t]
    states = [y]
    dt = dt0
    while t < t_end:
        if t + dt > t_end: 
            dt = t_end - t
        k1 = vdp_deriv(t, y, mu)
        y_e = [y[0] + dt * k1[0], y[1] + dt * k1[1]]
        k2 = vdp_deriv(t + dt, y_e, mu)
        y_h = [y[0] + (dt / 2.0) * (k1[0] + k2[0]), y[1] + (dt / 2.0) * (k1[1] + k2[1])]

        error = max(abs(y_h[0] - y_e[0]), abs(y_h[1] - y_e[1]))

        if error < tol:
            t += dt
            y = y_h
            times.append(t)
            states.append(y)
            dt = min(dt * 1.5, 0.5)
        else:
            dt = max(dt * 0.5, 1e-4)
    return times, states

def interp1d_linear(times, y1, t_eval):
    res = []
    idx = 0
    n_times = len(times)
    for t in t_eval:
        while idx < n_times - 2 and times[idx+1] < t:
            idx += 1
        t0, t1 = times[idx], times[idx+1]
        y0, y1_val = y1[idx], y1[idx+1]
        # Linear interpolation
        val = y0 + (y1_val - y0) * (t - t0) / (t1 - t0)
        res.append(val)
    return res

def get_dom_freq(mu):
    times, states = adaptive_euler_heun_fixed(mu)
    y1 = [s[0] for s in states]

    # Uniform grid from 100.0 to 600.0 with dt=0.1 -> 5001 points
    t_uniform = [100.0 + i * 0.1 for i in range(5001)]
    y1_uniform = interp1d_linear(times, y1, t_uniform)

    N = len(y1_uniform)

    # To avoid O(N^2) pure Python DFT taking too long, we can use a simple Cooley-Tukey FFT 
    # for the next power of 2, or just evaluate the DFT since we know the frequency is around 0.140 Hz.
    # 0.140 Hz corresponds to k = 0.140 * N * dt = 0.140 * 5001 * 0.1 = 70.014 -> index 70
    # Let's just search in a narrow band around k=70 (e.g. k in [1, 250]) to be safe and fast.
    max_mag = -1.0
    peak_k = 0

    for k in range(1, 250):
        re = 0.0
        im = 0.0
        # Precompute angle multiplier
        mult = -2.0 * math.pi * k / N
        for n in range(N):
            angle = mult * n
            re += y1_uniform[n] * math.cos(angle)
            im += y1_uniform[n] * math.sin(angle)
        mag = re*re + im*im
        if mag > max_mag:
            max_mag = mag
            peak_k = k

    return peak_k / (N * 0.1)

def bisection_root(f, a, b, tol=1e-3):
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        # Fallback if no sign change is detected
        return a 
    while (b - a) / 2.0 > tol:
        c = (a + b) / 2.0
        fc = f(c)
        if fc == 0:
            return c
        elif fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    return (a + b) / 2.0

def test_mu_solution_exists():
    assert os.path.exists('/home/user/mu_solution.txt'), "The file /home/user/mu_solution.txt was not created."

def test_mu_solution_correctness():
    # Compute expected mu
    def obj(mu):
        return get_dom_freq(mu) - 0.140

    expected_mu = bisection_root(obj, 1.0, 2.0, tol=1e-4)
    expected_str = f"{expected_mu:.3f}"

    with open('/home/user/mu_solution.txt', 'r') as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected mu to be {expected_str}, but got {actual_str} in /home/user/mu_solution.txt."

def test_simulate_py_fixed():
    with open('/home/user/simulate.py', 'r') as f:
        content = f.read()

    assert "np.sum(y_h - y_e)" not in content, "The buggy error calculation `np.sum(y_h - y_e)` is still in simulate.py."
    assert "np.max(np.abs(" in content or "max(abs(" in content or "np.linalg.norm" in content, "The error calculation in simulate.py does not appear to compute the maximum absolute difference or a valid norm."