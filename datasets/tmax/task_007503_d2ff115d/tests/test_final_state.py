# test_final_state.py

import os
import csv
import pytest

def test_rust_project_exists():
    assert os.path.isdir("/home/user/sensor_pipeline"), "The Rust project directory '/home/user/sensor_pipeline' is missing."
    assert os.path.isfile("/home/user/sensor_pipeline/Cargo.toml"), "The Cargo.toml file is missing."
    assert os.path.isfile("/home/user/sensor_pipeline/src/main.rs"), "The src/main.rs file is missing."

def test_output_file_exists():
    assert os.path.isfile("/home/user/output/aggregated_temps.csv"), "The output file '/home/user/output/aggregated_temps.csv' is missing."

def test_output_file_contents():
    file_path = "/home/user/output/aggregated_temps.csv"

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The output CSV is empty."

    # Check headers
    assert rows[0] == ["location", "max_temp_f", "avg_temp_f"], f"Headers do not match expected. Got: {rows[0]}"

    # Parse data rows
    data = {}
    for row in rows[1:]:
        assert len(row) == 3, f"Row does not have 3 columns: {row}"
        location = row[0]
        max_temp = float(row[1])
        avg_temp = float(row[2])
        data[location] = (max_temp, avg_temp)

    # Expected data
    expected_data = {
        "Warehouse_A": (77.0, 72.5),
        "Warehouse_B": (86.0, 86.0),
        "Warehouse_C": (59.0, 54.5)
    }

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} data rows, got {len(data)}."

    for loc, (exp_max, exp_avg) in expected_data.items():
        assert loc in data, f"Location '{loc}' is missing from the output."
        act_max, act_avg = data[loc]
        assert abs(act_max - exp_max) < 1e-6, f"For {loc}, expected max_temp_f {exp_max}, got {act_max}"
        assert abs(act_avg - exp_avg) < 1e-6, f"For {loc}, expected avg_temp_f {exp_avg}, got {act_avg}"