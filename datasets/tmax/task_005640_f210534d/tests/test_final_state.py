# test_final_state.py

import os
import csv
import math
import pytest

def read_input_csv(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = []
        for row in reader:
            data.append([float(x) if x.strip() else None for x in row])
    return header, data

def calc_mean(col):
    vals = [x for x in col if x is not None]
    return sum(vals) / len(vals)

def calc_pop_std(col, mu):
    vals = [x for x in col if x is not None]
    return math.sqrt(sum((x - mu)**2 for x in vals) / len(vals))

def calc_sample_cov(col1, col2):
    mu1 = calc_mean(col1)
    mu2 = calc_mean(col2)
    return sum((x - mu1) * (y - mu2) for x, y in zip(col1, col2)) / (len(col1) - 1)

def compute_expected_data():
    input_path = "/home/user/sensor_data.csv"
    if not os.path.exists(input_path):
        return [], []

    header, data = read_input_csv(input_path)

    # Transpose to columns
    cols = list(map(list, zip(*data)))

    # 1. Impute
    for i in range(len(cols)):
        mu = calc_mean(cols[i])
        cols[i] = [x if x is not None else mu for x in cols[i]]

    # 2. Cap outliers
    for i in range(len(cols)):
        mu = calc_mean(cols[i])
        sigma = calc_pop_std(cols[i], mu)
        cols[i] = [max(mu - 2*sigma, min(mu + 2*sigma, x)) for x in cols[i]]

    # 3. Feature Engineering
    interaction = [t * p for t, p in zip(cols[0], cols[1])]
    cols.append(interaction)

    # 4. Standardize
    for i in range(len(cols)):
        mu = calc_mean(cols[i])
        sigma = calc_pop_std(cols[i], mu)
        cols[i] = [(x - mu) / sigma for x in cols[i]]

    # 5. Covariance
    cov_matrix = []
    for i in range(len(cols)):
        row = []
        for j in range(len(cols)):
            row.append(calc_sample_cov(cols[i], cols[j]))
        cov_matrix.append(row)

    # Transpose back to rows
    processed_data = list(map(list, zip(*cols)))

    return processed_data, cov_matrix

def test_executable_exists():
    assert os.path.exists("/home/user/etl_bin"), "Executable /home/user/etl_bin is missing."
    assert os.access("/home/user/etl_bin", os.X_OK), "/home/user/etl_bin is not executable."

def test_processed_data_csv():
    output_path = "/home/user/processed_data.csv"
    assert os.path.exists(output_path), f"{output_path} is missing."

    expected_data, _ = compute_expected_data()

    with open(output_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["temp", "pressure", "humidity", "temp_pressure_interaction"], "Header is incorrect."

        actual_data = []
        for row in reader:
            actual_data.append([float(x) for x in row])

    assert len(actual_data) == len(expected_data), "Number of rows in processed data is incorrect."

    for i, (actual_row, expected_row) in enumerate(zip(actual_data, expected_data)):
        for j, (actual_val, expected_val) in enumerate(zip(actual_row, expected_row)):
            assert math.isclose(actual_val, expected_val, abs_tol=1e-3), \
                f"Mismatch at row {i+1}, col {j}: expected {expected_val:.4f}, got {actual_val:.4f}"

def test_cov_matrix_txt():
    output_path = "/home/user/cov_matrix.txt"
    assert os.path.exists(output_path), f"{output_path} is missing."

    _, expected_cov = compute_expected_data()

    with open(output_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == len(expected_cov), "Number of rows in covariance matrix is incorrect."

    for i, (line, expected_row) in enumerate(zip(lines, expected_cov)):
        actual_row = [float(x) for x in line.split()]
        assert len(actual_row) == len(expected_row), f"Number of columns in covariance matrix row {i} is incorrect."

        for j, (actual_val, expected_val) in enumerate(zip(actual_row, expected_row)):
            assert math.isclose(actual_val, expected_val, abs_tol=1e-3), \
                f"Covariance mismatch at ({i}, {j}): expected {expected_val:.4f}, got {actual_val:.4f}"