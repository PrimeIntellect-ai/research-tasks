# test_final_state.py

import os
import json
import csv
import math
import pytest

def get_expected_ols():
    fasta_file = "/home/user/data/sequences.fasta"
    csv_file = "/home/user/data/growth_rates.csv"

    # Parse FASTA
    seqs = {}
    with open(fasta_file, "r") as f:
        current_id = None
        current_seq = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    seqs[current_id] = "".join(current_seq)
                current_id = line[1:].split()[0]
                current_seq = []
            else:
                current_seq.append(line.upper())
        if current_id is not None:
            seqs[current_id] = "".join(current_seq)

    # Calculate GC ratios, ignoring corrupted ones
    gc_ratios = {}
    for sid, seq in seqs.items():
        g = seq.count('G')
        c = seq.count('C')
        a = seq.count('A')
        t = seq.count('T')
        total = a + c + g + t
        if total > 0:
            gc_ratios[sid] = (g + c) / total

    # Parse CSV
    growth_rates = {}
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                try:
                    growth_rates[row[0]] = float(row[1])
                except ValueError:
                    continue

    # Match valid sequences with growth rates
    x_vals = []
    y_vals = []
    for sid, gc in gc_ratios.items():
        if sid in growth_rates:
            x_vals.append(gc)
            y_vals.append(growth_rates[sid])

    if not x_vals:
        raise ValueError("No valid sequences matched with growth rates.")

    # OLS computation
    x_mean = sum(x_vals) / len(x_vals)
    y_mean = sum(y_vals) / len(y_vals)

    cov = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))
    var = sum((x - x_mean)**2 for x in x_vals)

    b1 = cov / var
    b0 = y_mean - b1 * x_mean

    return round(b0, 4), round(b1, 4)

def test_model_results_exists():
    result_path = "/home/user/model_results.json"
    assert os.path.isfile(result_path), f"The output file {result_path} does not exist."

def test_model_results_values():
    result_path = "/home/user/model_results.json"
    assert os.path.isfile(result_path), f"The output file {result_path} does not exist."

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {result_path} does not contain valid JSON.")

    assert "beta_0" in data, "The JSON file is missing the 'beta_0' key."
    assert "beta_1" in data, "The JSON file is missing the 'beta_1' key."

    expected_b0, expected_b1 = get_expected_ols()

    assert math.isclose(data["beta_0"], expected_b0, abs_tol=0.0001), \
        f"Expected beta_0 to be {expected_b0}, but got {data['beta_0']}. Check if corrupted sequences were properly ignored."
    assert math.isclose(data["beta_1"], expected_b1, abs_tol=0.0001), \
        f"Expected beta_1 to be {expected_b1}, but got {data['beta_1']}. Check if corrupted sequences were properly ignored."