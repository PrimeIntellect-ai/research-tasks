# test_final_state.py
import os

def test_mean_energy_output():
    init_file = '/home/user/init.txt'
    out_file = '/home/user/mean_energy.txt'

    assert os.path.isfile(init_file), f"Missing {init_file}. The initial coordinates file must exist."
    assert os.path.isfile(out_file), f"Missing {out_file}. The simulation must output the mean energy to this file."

    x_sq_sum = 0.0
    y_sq_sum = 0.0
    count = 0
    with open(init_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                x, y = map(float, parts)
                x_sq_sum += x**2
                y_sq_sum += y**2
                count += 1

    assert count == 1000, f"Expected 1000 points in {init_file}, got {count}."

    mean_x_sq = x_sq_sum / count
    mean_y_sq = y_sq_sum / count

    # alpha_max = 0.02, alpha = 0.019
    # x_mult = 1 - 2(0.019) = 0.962
    # y_mult = 1 - 100(0.019) = -0.900
    x_mult_sq = (0.962)**200
    y_mult_sq = (-0.9)**200

    expected_mean_E = mean_x_sq * x_mult_sq + 50 * mean_y_sq * y_mult_sq
    expected_str = f"{expected_mean_E:.6f}"

    with open(out_file, 'r') as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected mean energy '{expected_str}' in {out_file}, but got '{actual_str}'."

def test_sim_c_exists():
    sim_file = '/home/user/sim.c'
    assert os.path.isfile(sim_file), f"Missing {sim_file}. The C source code file must exist."