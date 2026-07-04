# test_final_state.py

import os
import csv

def test_run_pipeline_script_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_cpp_file_exists():
    cpp_path = '/home/user/process_data.cpp'
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} does not exist."

def test_model_metrics_output():
    csv_path = '/home/user/data/sensors.csv'
    output_path = '/home/user/output/model_metrics.txt'

    assert os.path.isfile(csv_path), f"Data file {csv_path} does not exist."
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    # Calculate exact OLS values from the CSV
    x = []
    y = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x.append(float(row['temperature']))
            y.append(float(row['pressure']))

    n = len(x)
    assert n > 0, "CSV file has no data rows."

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = sum((xi - mean_x) ** 2 for xi in x)

    expected_m = numerator / denominator
    expected_c = mean_y - expected_m * mean_x

    expected_mse = sum((yi - (expected_m * xi + expected_c)) ** 2 for xi, yi in zip(x, y)) / n

    # Read the output file
    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {output_path}, found {len(lines)}."

    parsed_metrics = {}
    for line in lines:
        parts = line.split(':')
        assert len(parts) == 2, f"Invalid line format in output: '{line}'. Expected 'Key: Value'."
        key = parts[0].strip()
        try:
            val = float(parts[1].strip())
            parsed_metrics[key] = val
        except ValueError:
            assert False, f"Could not parse float value from line: '{line}'"

    assert 'Slope' in parsed_metrics, "Missing 'Slope' in output."
    assert 'Intercept' in parsed_metrics, "Missing 'Intercept' in output."
    assert 'MSE' in parsed_metrics, "Missing 'MSE' in output."

    # Check values with tolerance
    tolerance = 0.0002

    assert abs(parsed_metrics['Slope'] - expected_m) <= tolerance, \
        f"Slope is incorrect. Expected ~{expected_m:.4f}, got {parsed_metrics['Slope']}"

    assert abs(parsed_metrics['Intercept'] - expected_c) <= tolerance, \
        f"Intercept is incorrect. Expected ~{expected_c:.4f}, got {parsed_metrics['Intercept']}"

    assert abs(parsed_metrics['MSE'] - expected_mse) <= tolerance, \
        f"MSE is incorrect. Expected ~{expected_mse:.4f}, got {parsed_metrics['MSE']}"