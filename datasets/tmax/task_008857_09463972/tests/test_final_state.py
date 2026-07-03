# test_final_state.py

import os
import subprocess
import csv
import math
import pytest

WORK_DIR = "/home/user/perf_test"

def test_directory_exists():
    assert os.path.isdir(WORK_DIR), f"Directory {WORK_DIR} does not exist."

def test_files_exist():
    expected_files = [
        "numerical_engine.cpp",
        "orchestrator_executed.ipynb",
        "results.csv",
        "timing_plot.png"
    ]
    for f in expected_files:
        path = os.path.join(WORK_DIR, f)
        assert os.path.isfile(path), f"File {path} does not exist."

def test_cpp_compilation_and_math():
    cpp_file = os.path.join(WORK_DIR, "numerical_engine.cpp")
    test_bin = os.path.join(WORK_DIR, "test_engine")

    # Compile
    compile_cmd = ["g++", "-O3", cpp_file, "-o", test_bin]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Compilation failed:\n{result.stderr}"

    # Run with N=1000
    run_cmd = [test_bin, "1000"]
    result = subprocess.run(run_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Execution failed:\n{result.stderr}"

    output = result.stdout.strip()
    parts = output.split(",")
    assert len(parts) == 4, f"Output must be 4 comma-separated values, got: {output}"

    n_str, integral_str, derivative_str, time_str = parts

    assert n_str == "1000", f"Expected N=1000, got {n_str}"

    try:
        integral = float(integral_str)
        derivative = float(derivative_str)
        time_us = float(time_str)
    except ValueError:
        pytest.fail(f"Could not parse numeric values from output: {output}")

    # Analytical integral of x^3 - 2x^2 + x from 0 to 10 is 1883.333...
    assert math.isclose(integral, 1883.333, rel_tol=1e-2), f"Integral {integral} is not close to 1883.333"

    # Analytical derivative at x=5 is 56
    assert math.isclose(derivative, 56.0, rel_tol=1e-2), f"Derivative {derivative} is not close to 56.0"

def test_results_csv():
    csv_file = os.path.join(WORK_DIR, "results.csv")
    assert os.path.isfile(csv_file), f"CSV file {csv_file} does not exist."

    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 6, f"Expected 6 rows (1 header + 5 data) in CSV, got {len(rows)}"

    header = rows[0]
    expected_header = ["N", "Integral", "Derivative", "Time_us"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    expected_n = [10, 100, 1000, 10000, 100000]
    actual_n = []
    for row in rows[1:]:
        assert len(row) == 4, f"Row {row} does not have 4 columns"
        try:
            actual_n.append(int(row[0]))
        except ValueError:
            pytest.fail(f"Could not parse N value as integer: {row[0]}")

    assert actual_n == expected_n, f"Expected N values {expected_n}, got {actual_n}"