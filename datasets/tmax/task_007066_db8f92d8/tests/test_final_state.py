# test_final_state.py
import os
import csv
import pytest

def test_csv_output():
    csv_path = "/home/user/bulk_import.csv"
    assert os.path.exists(csv_path), f"Expected CSV file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"Path {csv_path} is not a file."

    expected_rows = [
        ["id", "name_ja", "seo_text", "price"],
        ["101", "ゲーミングマウス", "【大特価】ゲーミングマウスがたったの5000円！", "5000"],
        ["105", "デスク", "【大特価】デスクがたったの12000円！", "12000"]
    ]

    actual_rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # skip empty lines if any
                actual_rows.append(row)

    assert actual_rows == expected_rows, f"CSV content mismatch. Expected {expected_rows}, got {actual_rows}."

def test_rust_project_exists():
    project_path = "/home/user/etl_pipeline"
    assert os.path.exists(project_path), f"Rust project directory {project_path} does not exist."
    assert os.path.isdir(project_path), f"Path {project_path} is not a directory."
    cargo_toml_path = os.path.join(project_path, "Cargo.toml")
    assert os.path.exists(cargo_toml_path), f"Cargo.toml not found in {project_path}."