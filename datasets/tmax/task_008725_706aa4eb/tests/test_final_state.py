# test_final_state.py

import os
import csv
import pytest

REPORT_CSV_PATH = "/home/user/report.csv"
CARGO_TOML_PATH = "/home/user/sales_report/Cargo.toml"

def test_rust_project_exists():
    assert os.path.exists(CARGO_TOML_PATH), f"Rust project Cargo.toml not found at {CARGO_TOML_PATH}"

def test_cargo_toml_dependencies():
    with open(CARGO_TOML_PATH, "r") as f:
        content = f.read()

    # Simple checks for dependencies
    assert "rusqlite" in content, "rusqlite dependency missing in Cargo.toml"
    assert "0.29" in content or "0.29.0" in content, "rusqlite version 0.29.0 not found in Cargo.toml"
    assert "bundled" in content, "rusqlite 'bundled' feature missing in Cargo.toml"
    assert "csv" in content, "csv dependency missing in Cargo.toml"
    assert "1.3" in content or "1.3.0" in content, "csv version 1.3.0 not found in Cargo.toml"

def test_report_csv_content():
    assert os.path.exists(REPORT_CSV_PATH), f"Report CSV not found at {REPORT_CSV_PATH}"

    expected_data = [
        ["id", "name", "department_id", "total_sales", "dept_rank"],
        ["1", "Alice", "1", "510", "1"],
        ["2", "Bob", "2", "270", "1"],
        ["3", "Charlie", "3", "230", "1"],
        ["4", "Dave", "2", "100", "3"],
        ["5", "Eve", "2", "150", "2"],
        ["6", "Frank", "3", "200", "2"],
    ]

    with open(REPORT_CSV_PATH, "r", newline="") as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows in CSV, but got {len(actual_data)}"

    for i, (actual_row, expected_row) in enumerate(zip(actual_data, expected_data)):
        assert actual_row == expected_row, f"Row {i} mismatch in CSV. Expected {expected_row}, got {actual_row}"