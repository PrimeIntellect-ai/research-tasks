# test_final_state.py

import os
import numpy as np
import scipy.integrate as integrate
import pytest

def exact_f(x):
    return -10000.0 * np.exp(-10000.0 * (x - 0.5)**2)

def test_solution_format_and_metrics():
    solution_path = "/home/user/solution.txt"
    assert os.path.exists(solution_path), f"Solution file not found at {solution_path}"

    try:
        data = np.loadtxt(solution_path)
    except Exception as e:
        pytest.fail(f"Failed to load {solution_path}. Ensure it contains space-separated numbers. Error: {e}")

    assert data.ndim == 2, f"Expected 2 columns in {solution_path}, but got {data.ndim} dimensions."
    assert data.shape[1] == 2, f"Expected 2 columns (x, u) in {solution_path}, but got {data.shape[1]} columns."

    x_agent = data[:, 0]
    u_agent = data[:, 1]

    num_points = len(x_agent)
    assert num_points < 150, f"Too many grid points: {num_points}. Must be strictly < 150."

    assert np.all(np.diff(x_agent) > 0), "The x values in solution.txt must be sorted in strictly ascending order."

    # Compute exact solution using double integration
    x_fine = np.linspace(0, 1, 10000)
    f_fine = exact_f(x_fine)

    # Handle newer scipy versions where cumtrapz is renamed to cumulative_trapezoid
    if hasattr(integrate, 'cumulative_trapezoid'):
        cumtrapz_func = integrate.cumulative_trapezoid
    else:
        cumtrapz_func = integrate.cumtrapz

    u_prime = cumtrapz_func(f_fine, x_fine, initial=0)
    u_temp = cumtrapz_func(u_prime, x_fine, initial=0)

    # Apply Dirichlet boundary conditions: u(0) = 0, u(1) = 0
    u_exact = u_temp - x_fine * u_temp[-1]

    # Interpolate agent's solution onto the fine grid
    u_interp = np.interp(x_fine, x_agent, u_agent)

    # Calculate maximum absolute error
    max_err = np.max(np.abs(u_interp - u_exact))

    assert max_err <= 0.005, f"Max error is {max_err:.5f}, which exceeds the threshold of 0.005."