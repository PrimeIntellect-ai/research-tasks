# test_final_state.py

import os
import math
import subprocess
import pytest

def test_package_installed():
    """Verify that the libfftw3-dev package is installed."""
    result = subprocess.run(["dpkg", "-s", "libfftw3-dev"], capture_output=True, text=True)
    assert result.returncode == 0, "The package 'libfftw3-dev' is not installed."

def test_c_source_and_executable_exist():
    """Check that the C source code and compiled executable exist."""
    assert os.path.isfile("/home/user/generate_data.c"), "/home/user/generate_data.c does not exist."
    assert os.path.isfile("/home/user/generate_data"), "/home/user/generate_data executable does not exist."
    assert os.access("/home/user/generate_data", os.X_OK), "/home/user/generate_data is not executable."

def compute_expected_csv():
    """Compute the expected CSV output using the exact specified PRNG and math logic."""
    state = 42
    def next_rand():
        nonlocal state
        state = (state * 1103515245 + 12345) % 2147483648
        return state / 2147483648.0

    lines = []
    for id_val in range(100):
        A = 0.1 + 1.9 * next_rand()
        y = []
        for i in range(100):
            t = i * 0.01
            v = -A + 2.0 * A * next_rand()
            y.append(math.sin(2.0 * math.pi * 5.0 * t) + v)

        # Compute FFT magnitudes for k in [10, 40]
        # Equivalent to FFTW unnormalized real-to-complex 1D DFT
        M = []
        for k in range(10, 41):
            re = 0.0
            im = 0.0
            for n in range(100):
                angle = -2.0 * math.pi * k * n / 100.0
                re += y[n] * math.cos(angle)
                im += y[n] * math.sin(angle)
            M.append(math.sqrt(re*re + im*im))

        # Linear regression
        sum_x = 0.0
        sum_y = 0.0
        sum_xy = 0.0
        sum_xx = 0.0
        n_points = 31

        for i, k in enumerate(range(10, 41)):
            mag = M[i]
            sum_x += k
            sum_y += mag
            sum_xy += k * mag
            sum_xx += k * k

        mean_x = sum_x / n_points
        mean_y = sum_y / n_points

        numerator = sum_xy - n_points * mean_x * mean_y
        denominator = sum_xx - n_points * mean_x * mean_x
        m = numerator / denominator

        lines.append(f"{id_val},{A:.4f},{m:.4f}")

    return lines

def test_csv_output():
    """Verify that the generated CSV file matches the expected output exactly."""
    csv_path = "/home/user/training_metadata.csv"
    assert os.path.exists(csv_path), f"File {csv_path} was not generated."

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    expected_lines = compute_expected_csv()

    assert len(actual_lines) == len(expected_lines), \
        f"Expected {len(expected_lines)} lines in the CSV, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, \
            f"Mismatch at line {i+1} in {csv_path}:\nExpected: {expected}\nActual:   {actual}"