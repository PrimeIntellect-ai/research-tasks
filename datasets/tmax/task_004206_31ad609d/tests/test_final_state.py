# test_final_state.py

import os
import pytest

def get_expected_sum():
    nx = 100
    dx = 1.0 / (nx - 1)
    alpha = 0.1
    T = 0.5
    N = 981
    dt = T / N

    u = [0.0] * nx
    un = [0.0] * nx

    for i in range(nx):
        x = i * dx
        u[i] = x * (1.0 - x) * 4.0

    for n in range(N):
        for i in range(1, nx - 1):
            un[i] = u[i] + alpha * dt / (dx * dx) * (u[i+1] - 2.0*u[i] + u[i-1])
        un[0] = 0.0
        un[nx-1] = 0.0
        for i in range(nx):
            u[i] = un[i]

    # Standard sequential addition to match C behavior
    total_sum = 0.0
    for i in range(nx):
        total_sum += u[i]

    return f"{total_sum:.6f}"

def test_result_file_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_output = get_expected_sum()

    assert content == expected_output, f"Expected output '{expected_output}', but got '{content}' in {result_path}."

def test_sim_c_modified():
    sim_c_path = "/home/user/sim.c"
    assert os.path.isfile(sim_c_path), f"File {sim_c_path} does not exist."

    with open(sim_c_path, 'r') as f:
        content = f.read()

    # N should be at least 981. We'll just verify the file has been changed from N = 100
    assert "int N = 100;" not in content, "The value of N in sim.c was not changed from 100."