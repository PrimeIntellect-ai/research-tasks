# test_final_state.py

import os
import math
import csv
import re
import pytest

def solve_newton(a, b, c):
    x = 0.0
    for _ in range(100):
        fx = a * math.exp(x) + b * x - c
        if abs(fx) < 1e-6:
            break
        dfx = a * math.exp(x) + b
        x = x - fx / dfx
    return x

def compute_expected_metrics(raw_data, ref_data):
    computed_x = []
    for row in raw_data:
        x = solve_newton(row['a'], row['b'], row['c'])
        computed_x.append(x)

    ref_x = [row['ref_x'] for row in ref_data]

    n = len(computed_x)

    sorted_computed = sorted(computed_x)
    sorted_ref = sorted(ref_x)

    w1 = sum(abs(sc - sr) for sc, sr in zip(sorted_computed, sorted_ref)) / n

    mean_c = sum(computed_x) / n
    mean_r = sum(ref_x) / n

    var_c = sum((x - mean_c)**2 for x in computed_x) / (n - 1)
    var_r = sum((x - mean_r)**2 for x in ref_x) / (n - 1)

    t_stat = (mean_c - mean_r) / math.sqrt(var_c / n + var_r / n)

    return computed_x, w1, t_stat

def test_source_files_exist():
    """Check that the C++ source and Makefile exist."""
    assert os.path.isfile("/home/user/src/pipeline.cpp"), "Missing /home/user/src/pipeline.cpp"
    assert os.path.isfile("/home/user/src/Makefile"), "Missing /home/user/src/Makefile"

    with open("/home/user/src/Makefile", "r") as f:
        makefile_content = f.read()
    assert "g++" in makefile_content, "Makefile does not appear to use g++."

def test_processed_csv():
    """Verify the computed roots in processed.csv."""
    processed_file = "/home/user/data/processed.csv"
    assert os.path.isfile(processed_file), f"Missing {processed_file}"

    raw_file = "/home/user/data/raw_data.csv"
    raw_data = []
    with open(raw_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_data.append({
                'id': int(row['id']),
                'a': float(row['a']),
                'b': float(row['b']),
                'c': float(row['c'])
            })

    expected_x = {row['id']: solve_newton(row['a'], row['b'], row['c']) for row in raw_data}

    with open(processed_file, "r") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["id", "computed_x"], "Header of processed.csv must be 'id,computed_x'"

        for row in reader:
            row_id = int(row['id'])
            comp_x = float(row['computed_x'])
            assert row_id in expected_x, f"Unexpected id {row_id} in processed.csv"
            assert math.isclose(comp_x, expected_x[row_id], abs_tol=1e-4), \
                f"Computed x for id {row_id} is {comp_x}, expected {expected_x[row_id]}"

def test_report_metrics():
    """Verify the calculated metrics in report.txt."""
    report_file = "/home/user/data/report.txt"
    assert os.path.isfile(report_file), f"Missing {report_file}"

    raw_file = "/home/user/data/raw_data.csv"
    ref_file = "/home/user/data/ref_states.csv"

    raw_data = []
    with open(raw_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_data.append({
                'id': int(row['id']),
                'a': float(row['a']),
                'b': float(row['b']),
                'c': float(row['c'])
            })

    ref_data = []
    with open(ref_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ref_data.append({
                'id': int(row['id']),
                'ref_x': float(row['ref_x'])
            })

    _, expected_w1, expected_t = compute_expected_metrics(raw_data, ref_data)

    with open(report_file, "r") as f:
        content = f.read()

    w1_match = re.search(r"Wasserstein Distance:\s*([+-]?\d*\.\d+)", content)
    assert w1_match is not None, "Could not find 'Wasserstein Distance: <value>' in report.txt"
    w1_val = float(w1_match.group(1))
    assert math.isclose(w1_val, expected_w1, abs_tol=1e-3), \
        f"Wasserstein Distance is {w1_val}, expected ~{expected_w1}"

    t_match = re.search(r"T-Statistic:\s*([+-]?\d*\.\d+)", content)
    assert t_match is not None, "Could not find 'T-Statistic: <value>' in report.txt"
    t_val = float(t_match.group(1))
    assert math.isclose(t_val, expected_t, abs_tol=1e-2), \
        f"T-Statistic is {t_val}, expected ~{expected_t}"