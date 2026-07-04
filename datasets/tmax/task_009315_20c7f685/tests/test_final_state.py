# test_final_state.py
import os
import re
import pytest

def rk4_step(x, v, dt):
    def fx(v_): return v_
    def fv(x_, v_): return -0.2*v_ - x_

    k1x = fx(v)
    k1v = fv(x, v)

    k2x = fx(v + 0.5*dt*k1v)
    k2v = fv(x + 0.5*dt*k1x, v + 0.5*dt*k1v)

    k3x = fx(v + 0.5*dt*k2v)
    k3v = fv(x + 0.5*dt*k2x, v + 0.5*dt*k2v)

    k4x = fx(v + dt*k3v)
    k4v = fv(x + dt*k3x, v + dt*k3v)

    x_new = x + (dt/6.0)*(k1x + 2*k2x + 2*k3x + k4x)
    v_new = v + (dt/6.0)*(k1v + 2*k2v + 2*k3v + k4v)
    return x_new, v_new

def get_expected_values():
    x, v = 1.0, 0.0
    dt = 0.1
    for _ in range(100):
        x, v = rk4_step(x, v, dt)
    return x, v

def test_sim_directory_exists():
    assert os.path.isdir("/home/user/sim"), "/home/user/sim directory does not exist."

def test_solver_c_exists():
    assert os.path.isfile("/home/user/sim/solver.c"), "/home/user/sim/solver.c does not exist."

def test_run_sim_executable_exists():
    executable_path = "/home/user/sim/run_sim"
    assert os.path.isfile(executable_path), f"{executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_final_state_file_contents():
    file_path = "/home/user/sim/final_state.txt"
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content, f"{file_path} is empty."

    # Parse the output
    match = re.match(r"^t=10\.00000,\s*x=([+-]?\d+\.\d+),\s*v=([+-]?\d+\.\d+)$", content)
    assert match is not None, f"Content of {file_path} does not match the required format. Got: {content}"

    actual_x = float(match.group(1))
    actual_v = float(match.group(2))

    expected_x, expected_v = get_expected_values()

    # Check within tolerance
    tolerance = 0.00002
    assert abs(actual_x - expected_x) <= tolerance, f"x value {actual_x} is not within {tolerance} of expected {expected_x:.5f}."
    assert abs(actual_v - expected_v) <= tolerance, f"v value {actual_v} is not within {tolerance} of expected {expected_v:.5f}."