# test_final_state.py

import os
import csv
import pytest

CARGO_TOML_PATH = "/home/user/graph_analyzer/Cargo.toml"
MAIN_RS_PATH = "/home/user/graph_analyzer/src/main.rs"
CSV_PATH = "/home/user/derivation_report.csv"

def test_cargo_project_exists():
    assert os.path.exists(CARGO_TOML_PATH), f"Cargo.toml missing at {CARGO_TOML_PATH}"
    assert os.path.exists(MAIN_RS_PATH), f"src/main.rs missing at {MAIN_RS_PATH}"

def test_rusqlite_dependency():
    with open(CARGO_TOML_PATH, "r") as f:
        content = f.read()
    assert "rusqlite" in content, "rusqlite dependency not found in Cargo.toml"

def test_csv_output():
    assert os.path.exists(CSV_PATH), f"CSV output missing at {CSV_PATH}"

    with open(CSV_PATH, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty"

    header = rows[0]
    expected_header = ["name", "domain", "size_mb", "path_length", "domain_rank"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    data_rows = rows[1:]

    # Expected data
    expected_data = [
        ["Embeddings_Filtered", "ML", "1000", "4", "2"],
        ["Images_Filtered", "CV", "2000", "2", "2"],
        ["Images_Resized", "CV", "2000", "3", "2"]
    ]

    # Ensure it's sorted alphabetically by name
    sorted_data_rows = sorted(data_rows, key=lambda x: x[0])
    assert data_rows == sorted_data_rows, "CSV rows are not sorted alphabetically by name"

    # Check contents
    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} rows, got {len(data_rows)}"

    for expected, actual in zip(expected_data, data_rows):
        assert actual == expected, f"Expected row {expected}, got {actual}"