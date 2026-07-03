# test_final_state.py

import os
import json
import csv
import math
import pytest

PARAMS_FILE = "/home/user/params.json"
RESULTS_FILE = "/home/user/results.csv"
SIMULATE_SCRIPT = "/home/user/simulate.py"
FASTA_FILE = "/home/user/target.fasta"

def compute_expected_params():
    if not os.path.exists(FASTA_FILE):
        return 0.65, 1.3
    with open(FASTA_FILE, 'r') as f:
        lines = [line.strip() for line in f if not line.startswith('>')]
    seq = "".join(lines).upper()
    if not seq:
        return 0.65, 1.3
    gc_count = seq.count('G') + seq.count('C')
    gc_frac = gc_count / len(seq)
    r = 2.0 * gc_frac
    return gc_frac, r

def test_simulate_script_exists():
    assert os.path.isfile(SIMULATE_SCRIPT), f"Script {SIMULATE_SCRIPT} is missing."

def test_params_json_correct():
    assert os.path.isfile(PARAMS_FILE), f"File {PARAMS_FILE} is missing."
    with open(PARAMS_FILE, 'r') as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{PARAMS_FILE} is not valid JSON.")

    assert "gc_fraction" in params, "Key 'gc_fraction' missing in params.json."
    assert "r" in params, "Key 'r' missing in params.json."

    expected_gc, expected_r = compute_expected_params()

    assert math.isclose(params["gc_fraction"], expected_gc, rel_tol=1e-4), f"Expected gc_fraction ~{expected_gc}, got {params['gc_fraction']}"
    assert math.isclose(params["r"], expected_r, rel_tol=1e-4), f"Expected r ~{expected_r}, got {params['r']}"

def test_results_csv_correct():
    assert os.path.isfile(RESULTS_FILE), f"File {RESULTS_FILE} is missing."

    with open(RESULTS_FILE, 'r') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"{RESULTS_FILE} is empty.")

        assert headers == ["t", "y_num", "y_exact"], f"Incorrect headers. Expected ['t', 'y_num', 'y_exact'], got {headers}"

        rows = list(reader)

    assert len(rows) == 11, f"Expected 11 rows (t=0..10), got {len(rows)}"

    _, expected_r = compute_expected_params()
    K = 1000.0
    y0 = 1.0

    for i, row in enumerate(rows):
        assert len(row) == 3, f"Row {i} does not have exactly 3 columns."
        try:
            t = float(row[0])
            y_num = float(row[1])
            y_exact = float(row[2])
        except ValueError:
            pytest.fail(f"Non-numeric values in row {i}: {row}")

        assert math.isclose(t, i, abs_tol=1e-5), f"Expected t={i}, got {t}"

        # Calculate true analytical
        true_exact = K / (1 + (K / y0 - 1) * math.exp(-expected_r * t))

        assert math.isclose(y_exact, true_exact, rel_tol=1e-2), f"At t={t}, expected y_exact ~{true_exact}, got {y_exact}"

        # Check numerical error < 1%
        error = abs(y_num - true_exact) / true_exact
        assert error < 0.01, f"At t={t}, numerical value {y_num} differs from exact {true_exact} by >= 1% (error: {error:.2%})"