# test_final_state.py

import csv
import math
import os

def compute_expected_cleaned_data():
    input_path = '/home/user/sensor_data.csv'
    assert os.path.exists(input_path), f"Input file {input_path} is missing."

    with open(input_path, 'r') as f:
        reader = csv.DictReader(f)
        data = [(float(row['X']), float(row['Y'])) for row in reader]

    N = len(data)
    assert N > 0, "Input data is empty."

    sum_x = sum(x for x, y in data)
    sum_y = sum(y for x, y in data)
    sum_xy = sum(x * y for x, y in data)
    sum_x2 = sum(x**2 for x, y in data)

    m = (N * sum_xy - sum_x * sum_y) / (N * sum_x2 - sum_x**2)
    c = (sum_y - m * sum_x) / N

    residuals = [y - (m * x + c) for x, y in data]
    variance = sum(r**2 for r in residuals) / N
    std_dev = math.sqrt(variance)

    cleaned = []
    for i, (x, y) in enumerate(data):
        if abs(residuals[i]) <= 2 * std_dev:
            cleaned.append((x, y))

    return cleaned

def test_cleaned_data_csv():
    output_path = '/home/user/cleaned_data.csv'
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    expected_data = compute_expected_cleaned_data()

    with open(output_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"File {output_path} is empty."
    assert lines[0] == "X,Y", f"Header in {output_path} is incorrect. Expected 'X,Y', got '{lines[0]}'."

    actual_data = lines[1:]
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} data rows, got {len(actual_data)}."

    for i, (expected_x, expected_y) in enumerate(expected_data):
        expected_line = f"{expected_x:.1f},{expected_y:.1f}"
        assert actual_data[i] == expected_line, f"Row {i+1} mismatch. Expected '{expected_line}', got '{actual_data[i]}'."

def test_benchmark_output():
    bench_path = '/home/user/benchmark.txt'
    assert os.path.exists(bench_path), f"Benchmark output file {bench_path} is missing."

    with open(bench_path, 'r') as f:
        content = f.read()

    assert 'BenchmarkInference' in content, f"'BenchmarkInference' not found in {bench_path}."
    assert 'ns/op' in content, f"'ns/op' not found in {bench_path}."