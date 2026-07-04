# test_final_state.py

import os
import pytest

def compute_expected_posterior(csv_path):
    if not os.path.exists(csv_path):
        return None

    sum_prec = 1.0
    sum_prec_x = 0.0
    sum_prec_y = 0.0

    with open(csv_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        return None

    # Skip header
    for line in lines[1:]:
        parts = line.strip().split(',')
        if len(parts) != 4:
            continue
        try:
            sensor_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            variance = float(parts[3])
        except ValueError:
            continue

        if variance <= 0:
            continue

        prec = 1.0 / variance
        sum_prec += prec
        sum_prec_x += prec * x
        sum_prec_y += prec * y

    post_x = sum_prec_x / sum_prec
    post_y = sum_prec_y / sum_prec

    return f"{post_x:.4f},{post_y:.4f}"

def test_files_exist():
    assert os.path.isfile("/home/user/processor.c"), "/home/user/processor.c is missing."
    assert os.path.isfile("/home/user/Makefile"), "/home/user/Makefile is missing."
    assert os.path.isfile("/home/user/processor"), "The executable /home/user/processor is missing. Did 'make all' run successfully?"
    assert os.path.isfile("/home/user/posterior.txt"), "/home/user/posterior.txt is missing. Did 'make run' execute successfully?"

def test_posterior_output():
    csv_path = "/home/user/data.csv"
    posterior_path = "/home/user/posterior.txt"

    expected_output = compute_expected_posterior(csv_path)
    assert expected_output is not None, "Could not compute expected posterior from data.csv."

    with open(posterior_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Output in posterior.txt is incorrect. Expected '{expected_output}', got '{actual_output}'."