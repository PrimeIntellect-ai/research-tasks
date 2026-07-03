# test_final_state.py
import os
import json
import numpy as np
from scipy.integrate import solve_ivp
import pytest

def test_result_spectrum_mse():
    result_file = '/home/user/result_spectrum.json'
    assert os.path.isfile(result_file), f"Result file {result_file} is missing. Did the worker submit the result?"

    with open(result_file, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_file} does not contain valid JSON.")

    agent_data = np.array(agent_data)
    assert agent_data.ndim == 1, "Submitted data must be a 1D list of amplitudes."
    assert len(agent_data) == 501, f"Expected 501 amplitudes, got {len(agent_data)}."

    # Compute golden reference
    alpha = 0.05
    duration = 10.0
    dt = 0.01
    Nx = 101
    x = np.linspace(0, 1, Nx)
    dx = x[1] - x[0]
    t_eval = np.arange(0, duration + dt/2, dt) # 1001 points

    def pde_enforced(t, u_int):
        u = np.zeros(Nx)
        u[1:-1] = u_int
        u[0] = np.sin(15*t) + 0.5*np.sin(40*t)
        u[-1] = 0

        dudt = np.zeros(Nx)
        dudt[1:-1] = alpha * (u[2:] - 2*u[1:-1] + u[:-2]) / dx**2
        return dudt[1:-1]

    u0 = np.zeros(Nx-2)
    sol = solve_ivp(pde_enforced, [0, duration], u0, t_eval=t_eval, method='BDF')

    u_full = np.zeros((Nx, len(t_eval)))
    u_full[0, :] = np.sin(15*t_eval) + 0.5*np.sin(40*t_eval)
    u_full[-1, :] = 0
    u_full[1:-1, :] = sol.y

    # Sensor at x=0.5 is index 50
    sensor_signal = u_full[50, :]

    # Compute FFT
    spectrum = np.abs(np.fft.fft(sensor_signal)) / len(sensor_signal)
    half_len = len(sensor_signal) // 2 + 1
    golden_amplitudes = spectrum[:half_len] # length 501

    # Calculate MSE
    mse = np.mean((agent_data - golden_amplitudes)**2)
    threshold = 1e-4

    assert mse < threshold, f"MSE {mse:.6e} is not strictly less than the threshold {threshold}."