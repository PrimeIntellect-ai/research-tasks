# test_final_state.py

import os
import math
import pytest

def test_spectral_result():
    profile_path = "/home/user/thermal_profile.txt"
    result_path = "/home/user/spectral_result.txt"

    assert os.path.exists(profile_path), f"Input file {profile_path} is missing. Did you delete it?"
    assert os.path.exists(result_path), f"Output file {result_path} is missing. Did you create it?"

    # Read SensorB_Temp (3rd column)
    A = []
    with open(profile_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                try:
                    A.append(float(parts[2]))
                except ValueError:
                    continue

    N = len(A)
    assert N > 0, f"No valid data found in {profile_path}"

    # 1. ODE Solver (Euler method)
    E = [0.0] * N
    E[0] = A[0]
    k = 0.05
    T_env = 25
    dt = 1

    for n in range(0, N-1):
        E[n+1] = E[n] - k * (E[n] - T_env) * dt

    # 2. Residuals
    R = [A[n] - E[n] for n in range(N)]

    # 3. DFT at k_freq = 2
    k_freq = 2
    Re = 0.0
    Im = 0.0

    for n in range(N):
        angle = 2 * math.pi * k_freq * n / N
        Re += R[n] * math.cos(angle)
        Im += R[n] * math.sin(-angle)

    magnitude = math.sqrt(Re**2 + Im**2)
    expected_result = f"{magnitude:.3f}"

    with open(result_path, 'r') as f:
        actual_result = f.read().strip()

    assert actual_result == expected_result, (
        f"Incorrect result in {result_path}. "
        f"Expected '{expected_result}', but found '{actual_result}'."
    )