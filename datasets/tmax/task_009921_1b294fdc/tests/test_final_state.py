# test_final_state.py

import os
import re
import subprocess
import sys

def test_cpp_updated():
    file_path = "/home/user/heat_sim.cpp"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read()

    assert "double dt = 0.001;" not in content, "The file still contains the hardcoded buggy dt variable."
    assert "dt =" in content, "The file must calculate dt."

def test_output_exists_and_valid():
    output_path = "/home/user/output.csv"
    assert os.path.exists(output_path), f"File {output_path} does not exist. Did you run the simulation?"

    with open(output_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) == 2500, f"The file {output_path} should contain exactly 2500 lines, but found {len(lines)}."

    # Check that they are valid floats and not NaN
    for i, line in enumerate(lines):
        try:
            val = float(line)
            assert val == val, f"Found NaN value at line {i+1} in {output_path}."
        except ValueError:
            raise AssertionError(f"Invalid float value at line {i+1} in {output_path}: {line}")

def test_report_correct():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"File {report_path} does not exist."

    with open(report_path, 'r') as f:
        content = f.read()

    match = re.search(r'CI:\s*\[([0-9.]+),\s*([0-9.]+)\]', content)
    assert match is not None, "Could not parse CI from report.txt. Expected format: CI: [lower_bound, upper_bound]"

    lower = float(match.group(1))
    upper = float(match.group(2))

    # Use a subprocess to run the numpy verification script so we strictly adhere to stdlib imports in this pytest file
    script = """
import numpy as np
with open('/home/user/output.csv', 'r') as f:
    out_vals = np.array([float(x) for x in f.read().splitlines()])
with open('/home/user/reference.csv', 'r') as f:
    ref_vals = np.array([float(x) for x in f.read().splitlines()])
residuals = np.abs(out_vals - ref_vals)
np.random.seed(42)
means = [np.mean(np.random.choice(residuals, size=len(residuals), replace=True)) for _ in range(10000)]
print(np.percentile(means, 2.5))
print(np.percentile(means, 97.5))
"""
    try:
        output = subprocess.check_output([sys.executable, "-c", script], stderr=subprocess.STDOUT).decode('utf-8').split()
        expected_lower = float(output[0])
        expected_upper = float(output[1])
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"Failed to compute expected CI using numpy: {e.output.decode('utf-8')}")
    except Exception as e:
        raise AssertionError(f"Failed to compute expected CI: {e}")

    assert abs(lower - expected_lower) < 1e-5, f"Lower bound {lower} does not match expected {expected_lower:.6f}"
    assert abs(upper - expected_upper) < 1e-5, f"Upper bound {upper} does not match expected {expected_upper:.6f}"