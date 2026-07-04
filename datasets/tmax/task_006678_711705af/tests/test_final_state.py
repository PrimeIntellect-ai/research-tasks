# test_final_state.py

import os
import pytest

def test_c_file_exists():
    c_path = "/home/user/bootstrap.c"
    assert os.path.exists(c_path), f"The C source file {c_path} does not exist."
    assert os.path.isfile(c_path), f"{c_path} is not a file."

def test_output_file_exists():
    out_path = "/home/user/ci_output.txt"
    assert os.path.exists(out_path), f"The output file {out_path} does not exist."
    assert os.path.isfile(out_path), f"{out_path} is not a file."

def test_ci_output_content():
    csv_path = "/home/user/sensor_data.csv"
    assert os.path.exists(csv_path), f"{csv_path} is missing."

    x_vals = []
    y_vals = []
    with open(csv_path, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            if not line.strip():
                continue
            x, y = line.strip().split(",")
            x_vals.append(float(x))
            y_vals.append(float(y))

    assert len(x_vals) == 100, f"Expected exactly 100 data points in {csv_path}, found {len(x_vals)}."

    # Recompute the expected confidence interval based on the actual data
    state = 42
    def get_random_index(num_points=100):
        nonlocal state
        state = (1103515245 * state + 12345) % 2147483648
        return state % num_points

    slopes = []
    for _ in range(10000):
        samp_x = []
        samp_y = []
        for _ in range(100):
            idx = get_random_index(100)
            samp_x.append(x_vals[idx])
            samp_y.append(y_vals[idx])

        n = 100
        sum_x = sum(samp_x)
        sum_y = sum(samp_y)
        sum_xy = sum(x * y for x, y in zip(samp_x, samp_y))
        sum_xx = sum(x * x for x in samp_x)

        denominator = n * sum_xx - sum_x**2
        if denominator == 0:
            slope = 0.0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / denominator
        slopes.append(slope)

    slopes.sort()
    lower_bound = slopes[249]
    upper_bound = slopes[9749]

    expected_output = f"Slope CI: [{lower_bound:.4f}, {upper_bound:.4f}]"

    out_path = "/home/user/ci_output.txt"
    with open(out_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Content of {out_path} is incorrect. "
        f"Expected '{expected_output}', but got '{actual_output}'."
    )