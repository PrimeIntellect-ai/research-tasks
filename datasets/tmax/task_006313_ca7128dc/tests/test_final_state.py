# test_final_state.py
import os
import re

def f(t, y):
    return -20.0 * (y - t**2) + 2.0 * t

def compute_expected_w1():
    h = 0.04
    steps = 25
    N = 1000
    w1_sum = 0.0

    for i in range(N):
        y0 = i * 0.001

        # Euler
        y_e = y0
        t = 0.0
        for _ in range(steps):
            y_e = y_e + h * f(t, y_e)
            t += h

        # RK4
        y_r = y0
        t = 0.0
        for _ in range(steps):
            k1 = f(t, y_r)
            k2 = f(t + h/2.0, y_r + h*k1/2.0)
            k3 = f(t + h/2.0, y_r + h*k2/2.0)
            k4 = f(t + h, y_r + h*k3)
            y_r = y_r + (h/6.0)*(k1 + 2.0*k2 + 2.0*k3 + k4)
            t += h

        w1_sum += abs(y_e - y_r)

    return w1_sum / N

def test_profile_results_exists():
    assert os.path.exists("/home/user/profile_results.txt"), "The file /home/user/profile_results.txt does not exist."

def test_profile_results_content():
    with open("/home/user/profile_results.txt", "r") as f:
        content = f.read()

    # Check Euler_stable
    assert re.search(r"Euler_stable:\s*yes", content), "The output must specify 'Euler_stable: yes'"

    # Check W1_distance
    expected_w1 = compute_expected_w1()
    expected_str = f"{expected_w1:.6f}"

    match = re.search(r"W1_distance:\s*([0-9\.]+)", content)
    assert match is not None, "Could not find 'W1_distance: [value]' in the output file."

    actual_str = match.group(1)

    assert actual_str == expected_str, f"W1_distance is incorrect. Expected {expected_str}, but got {actual_str}."