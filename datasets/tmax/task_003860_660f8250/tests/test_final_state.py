# test_final_state.py

import os
import math

def test_rust_project_exists():
    """Check if the Rust project was created."""
    cargo_toml = "/home/user/sensor_analysis/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Rust project file {cargo_toml} does not exist. Did you create the Cargo project?"

def test_correlation_file_exists():
    """Check if the output file exists."""
    output_file = "/home/user/sensor_analysis/correlation.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

def test_correlation_value():
    """Check if the correlation value is correct."""
    # Compute the expected correlation dynamically
    X = [20.5, 22.1, 19.8, 23.0, 24.5, 18.0, 19.2, 25.1]
    Y = [45.0, 48.2, 43.5, 52.0, 55.5, 40.0, 42.1, 58.0]

    n = len(X)
    sum_x = sum(X)
    sum_y = sum(Y)
    sum_x_sq = sum(x**2 for x in X)
    sum_y_sq = sum(y**2 for y in Y)
    sum_xy = sum(x*y for x, y in zip(X, Y))

    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))
    r = numerator / denominator

    expected_value = f"{r:.4f}"

    output_file = "/home/user/sensor_analysis/correlation.txt"
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == expected_value, f"Expected correlation value '{expected_value}', but got '{content}'."