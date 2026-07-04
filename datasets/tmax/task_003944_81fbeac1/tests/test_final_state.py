# test_final_state.py

import os
import csv
import math

def solve_kepler(a, b, tol=1e-6):
    x = b
    while True:
        f_x = x - a * math.sin(x) - b
        if abs(f_x) < tol:
            break
        f_prime_x = 1 - a * math.cos(x)
        x = x - f_x / f_prime_x
    return x

def test_c_file_exists():
    """Check if the C source file was created."""
    c_file = '/home/user/generate_labels.c'
    assert os.path.exists(c_file), f"Expected C program at {c_file} is missing."
    assert os.path.isfile(c_file), f"Path {c_file} is not a file."

def test_training_data_exists_and_correct():
    """Check if training_data.csv exists and has the correct computed values."""
    csv_file = '/home/user/training_data.csv'
    assert os.path.exists(csv_file), f"Expected output file at {csv_file} is missing."
    assert os.path.isfile(csv_file), f"Path {csv_file} is not a file."

    expected_inputs = [
        (1, 0.5, 1.0),
        (2, 0.1, 2.0),
        (3, 0.8, 0.5),
        (4, 0.9, 3.1),
        (5, 0.25, 1.5)
    ]

    with open(csv_file, 'r') as f:
        reader = list(csv.reader(f))

    assert len(reader) == 5, f"Expected 5 rows in {csv_file}, but found {len(reader)}."

    for i, row in enumerate(reader):
        assert len(row) == 4, f"Row {i+1} does not have exactly 4 columns: {row}"

        try:
            r_id = int(row[0])
            r_a = float(row[1])
            r_b = float(row[2])
            r_x = float(row[3])
        except ValueError:
            assert False, f"Row {i+1} contains non-numeric data: {row}"

        exp_id, exp_a, exp_b = expected_inputs[i]
        assert r_id == exp_id, f"Row {i+1} ID mismatch. Expected {exp_id}, got {r_id}"
        assert abs(r_a - exp_a) < 1e-9, f"Row {i+1} 'a' mismatch. Expected {exp_a}, got {r_a}"
        assert abs(r_b - exp_b) < 1e-9, f"Row {i+1} 'b' mismatch. Expected {exp_b}, got {r_b}"

        exp_x = solve_kepler(exp_a, exp_b)

        # The output must be printed with exactly 6 decimal places, so we check string representation
        expected_x_str = f"{exp_x:.6f}"
        assert row[3].strip() == expected_x_str, f"Row {i+1} 'x' mismatch. Expected {expected_x_str}, got {row[3]}"