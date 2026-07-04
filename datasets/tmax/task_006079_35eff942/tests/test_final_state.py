# test_final_state.py

import os
import math
import pytest

def get_expected_solution():
    alpha = 0.04
    # Find the minimum N >= 10 and corresponding minimum stable M
    for N in range(10, 100):
        # Stability condition for FTCS: r = alpha * dt / dx^2 <= 0.5
        # dt = 0.5 / M, dx = 1.0 / N
        # r = alpha * (0.5 / M) * N^2 <= 0.5
        # M >= alpha * N^2
        M = math.ceil(alpha * N**2)
        if M == 0:
            M = 1

        # Simulate
        dx = 1.0 / N
        dt = 0.5 / M
        r = alpha * dt / (dx**2)

        u = [math.sin(math.pi * i * dx) for i in range(N + 1)]
        for _ in range(M):
            u_new = u[:]
            for i in range(1, N):
                u_new[i] = u[i] + r * (u[i+1] - 2.0 * u[i] + u[i-1])
            u = u_new

        # Check max absolute error vs analytical
        max_err = 0.0
        for i in range(N + 1):
            x = i * dx
            exact = math.sin(math.pi * x) * math.exp(-alpha * math.pi**2 * 0.5)
            err = abs(u[i] - exact)
            if err > max_err:
                max_err = err

        if max_err < 0.005:
            return f"{alpha},{N},{M}"

def test_executable_compiled():
    exe_path = "/home/user/heat_sim"
    assert os.path.exists(exe_path), f"Executable {exe_path} was not found."
    assert os.path.isfile(exe_path), f"{exe_path} is not a file."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_solution_file():
    sol_path = "/home/user/solution.txt"
    assert os.path.exists(sol_path), f"Solution file {sol_path} was not found."

    with open(sol_path, "r") as f:
        agent_solution = f.read().strip()

    expected_solution = get_expected_solution()

    # Parse to allow for minor formatting differences like spaces
    try:
        agent_parts = [p.strip() for p in agent_solution.split(",")]
        expected_parts = expected_solution.split(",")

        assert float(agent_parts[0]) == float(expected_parts[0]), f"Expected alpha={expected_parts[0]}, got {agent_parts[0]}"
        assert int(agent_parts[1]) == int(expected_parts[1]), f"Expected N={expected_parts[1]}, got {agent_parts[1]}"
        assert int(agent_parts[2]) == int(expected_parts[2]), f"Expected M={expected_parts[2]}, got {agent_parts[2]}"
    except Exception as e:
        pytest.fail(f"Failed to parse or validate solution.txt. Expected format 'alpha,N,M' with values {expected_solution}. Got: '{agent_solution}'. Error: {e}")