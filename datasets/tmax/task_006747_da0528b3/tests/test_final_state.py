# test_final_state.py
import os
import csv
import json
import math

def test_rust_project_exists():
    cargo_toml_path = "/home/user/project/dim_reducer/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"Rust project 'dim_reducer' not found. Expected {cargo_toml_path} to exist."

def test_reduced_csv_valid():
    csv_path = "/home/user/data/reduced.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} is missing."

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 1000, f"Expected 1000 rows in reduced.csv, found {len(rows)}."

    for i, row in enumerate(rows):
        assert len(row) == 5, f"Expected 5 columns in row {i}, found {len(row)}."
        for val in row:
            try:
                f_val = float(val)
                assert not math.isnan(f_val), f"NaN value found in row {i}."
            except ValueError:
                assert False, f"Non-float value found in row {i}: {val}"

def test_experiment_log_valid():
    log_path = "/home/user/experiment_log.json"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{log_path} is not a valid JSON file."

    assert data.get("input_dim") == 50, f"Expected input_dim to be 50, got {data.get('input_dim')}."
    assert data.get("output_dim") == 5, f"Expected output_dim to be 5, got {data.get('output_dim')}."
    assert data.get("status") == "success", f"Expected status to be 'success', got {data.get('status')}."