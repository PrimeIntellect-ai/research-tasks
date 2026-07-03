# test_final_state.py

import os
import math
import pytest

def rk4_step(y, k, dt):
    def f(y_val):
        return k * y_val - 0.05 * y_val**2

    k1 = f(y)
    k2 = f(y + dt * k1 / 2)
    k3 = f(y + dt * k2 / 2)
    k4 = f(y + dt * k3)
    return y + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_population(dt):
    fasta_path = "/home/user/data/sequences.fasta"
    assert os.path.exists(fasta_path), f"Missing required file: {fasta_path}"

    with open(fasta_path, "r") as f:
        lines = f.readlines()

    k_values = []
    seq = ""
    for line in lines:
        if line.startswith(">"):
            if seq:
                gc = seq.count("G") + seq.count("C")
                k_values.append(gc / len(seq))
                seq = ""
        else:
            seq += line.strip()
    if seq:
        gc = seq.count("G") + seq.count("C")
        k_values.append(gc / len(seq))

    # Kahan Summation
    total_sum = 0.0
    c = 0.0

    for k in k_values:
        y = 2.0
        # To avoid floating point accumulation errors on t, 
        # we calculate number of steps
        steps = int(round(100.0 / dt))
        for _ in range(steps):
            y = rk4_step(y, k, dt)

        y_final = y
        y_kahan = y_final - c
        t_sum = total_sum + y_kahan
        c = (t_sum - total_sum) - y_kahan
        total_sum = t_sum

    return total_sum

@pytest.fixture(scope="session")
def expected_values():
    dt = 1.0
    prev_sum = simulate_population(dt)
    while True:
        next_dt = dt / 2.0
        curr_sum = simulate_population(next_dt)
        if abs(prev_sum - curr_sum) < 1e-5:
            chosen_dt = dt
            final_result = prev_sum
            break
        dt = next_dt
        prev_sum = curr_sum
    return chosen_dt, final_result

def test_c_program_exists():
    path = "/home/user/simulate.c"
    assert os.path.exists(path), f"The C program was not found at {path}."

def test_dt_chosen_file(expected_values):
    expected_dt, _ = expected_values
    expected_str = f"{expected_dt:.4f}"

    path = "/home/user/dt_chosen.txt"
    assert os.path.exists(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == expected_str, f"Expected step size {expected_str} in {path}, but got {content}."

def test_result_file(expected_values):
    _, expected_result = expected_values
    expected_str = f"{expected_result:.6f}"

    path = "/home/user/result.txt"
    assert os.path.exists(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == expected_str, f"Expected final concentration {expected_str} in {path}, but got {content}."