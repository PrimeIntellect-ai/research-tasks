# test_final_state.py

import os
import csv
import json
import stat
import pytest

def test_rust_project_exists():
    cargo_toml = "/home/user/sensor_pipeline/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"{cargo_toml} is missing. Did you create the Cargo project?"

def test_run_script_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_classified_results_correct():
    out_path = "/home/user/data/classified_results.csv"
    assert os.path.isfile(out_path), f"{out_path} is missing. Did the pipeline run correctly?"

    # Recompute expected truth
    weights_path = "/home/user/data/model_weights.json"
    raw_data_path = "/home/user/data/raw_sensor.csv"

    assert os.path.isfile(weights_path), f"Input file {weights_path} missing."
    assert os.path.isfile(raw_data_path), f"Input file {raw_data_path} missing."

    with open(weights_path, 'r') as f:
        W = json.load(f)

    expected_rows = []
    with open(raw_data_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            id_val = int(row[0])
            X = [float(x) for x in row[1:]]

            # Dimensionality reduction: Z = X * W
            Z = [0.0, 0.0]
            for i in range(10):
                Z[0] += X[i] * W[i][0]
                Z[1] += X[i] * W[i][1]

            # Log-likelihood calculations
            ll_0 = -0.5 * ((Z[0] - 0.0)**2 + (Z[1] - 0.0)**2)
            ll_1 = -0.5 * ((Z[0] - 2.0)**2 + (Z[1] - (-2.0))**2)

            assigned_class = 0 if ll_0 > ll_1 else 1
            max_ll = max(ll_0, ll_1)

            expected_rows.append([str(id_val), str(assigned_class), f"{max_ll:.4f}"])

    # Read actual results
    with open(out_path, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("The classified_results.csv file is empty.")

        assert header == ["id", "class", "max_ll"], f"Header mismatch: expected ['id', 'class', 'max_ll'], got {header}"

        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows of data, got {len(actual_rows)}."

    for i, (act, exp) in enumerate(zip(actual_rows, expected_rows)):
        assert act == exp, f"Row {i+1} mismatch: expected {exp}, got {act}. Ensure max_ll is rounded to 4 decimal places."