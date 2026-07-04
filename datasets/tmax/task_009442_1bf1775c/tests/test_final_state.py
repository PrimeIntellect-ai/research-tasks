# test_final_state.py

import os
import re

def test_c_source_exists():
    assert os.path.isfile("/home/user/generate_features.c"), "C source file /home/user/generate_features.c is missing."

def test_executable_exists():
    assert os.path.isfile("/home/user/generate_features"), "Executable /home/user/generate_features is missing."
    assert os.access("/home/user/generate_features", os.X_OK), "/home/user/generate_features is not executable."

def test_csv_exists_and_format():
    csv_path = "/home/user/ml_features.csv"
    assert os.path.isfile(csv_path), f"{csv_path} is missing."

    with open(csv_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, "CSV file is empty."
    header = lines[0].strip()
    assert header == "y_bin_center,pdf,pdf_derivative", f"Invalid CSV header: {header}"

    # 100 bins means 100 data lines + 1 header line = 101 lines
    data_lines = [line for line in lines[1:] if line.strip()]
    assert len(data_lines) == 100, f"Expected 100 data rows in CSV, found {len(data_lines)}."

    # Check that the first row is formatted correctly
    parts = data_lines[0].strip().split(',')
    assert len(parts) == 3, "Each data row must have 3 columns."
    try:
        float(parts[0])
        float(parts[1])
        float(parts[2])
    except ValueError:
        assert False, "CSV data rows must contain valid floats."

def test_summary_txt():
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"{summary_path} is missing."

    with open(summary_path, 'r') as f:
        content = f.read().strip()

    match = re.search(r'Integral:\s*([0-9.]+)', content)
    assert match is not None, "summary.txt does not contain 'Integral: <value>'."

    integral_val = float(match.group(1))
    assert 0.99 <= integral_val <= 1.01, f"Integral value {integral_val} is out of expected bounds (should be ~1.0)."

def test_gnuplot_script_exists():
    assert os.path.isfile("/home/user/plot_features.gp"), "Gnuplot script /home/user/plot_features.gp is missing."

def test_png_exists():
    assert os.path.isfile("/home/user/features.png"), "PNG image /home/user/features.png is missing."
    assert os.path.getsize("/home/user/features.png") > 0, "PNG image /home/user/features.png is empty."