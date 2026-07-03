# test_final_state.py

import os
import csv

def test_rust_project_exists():
    assert os.path.isdir("/home/user/etl_rust"), "Rust project directory /home/user/etl_rust is missing."
    assert os.path.exists("/home/user/etl_rust/Cargo.toml"), "Cargo.toml is missing in /home/user/etl_rust."

def test_selected_features_output():
    output_path = "/home/user/selected_features.csv"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r", newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Output CSV is empty."

    header = rows[0]
    assert len(header) == 2, f"Expected 2 columns in output, found {len(header)}."

    # Check that columns are f2 and f5
    assert set(header) == {"f2", "f5"}, f"Expected columns 'f2' and 'f5', found {header}."

    # Determine indices
    f2_idx = header.index("f2")
    f5_idx = header.index("f5")

    expected_f2 = ["100", "110", "120", "110", "130", "105"]
    expected_f5 = ["5000", "5500", "5100", "5200", "5100", "5000"]

    data_rows = rows[1:]
    assert len(data_rows) == 6, f"Expected 6 data rows, found {len(data_rows)}."

    actual_f2 = [row[f2_idx] for row in data_rows]
    actual_f5 = [row[f5_idx] for row in data_rows]

    assert actual_f2 == expected_f2, f"Column f2 values are incorrect. Expected {expected_f2}, got {actual_f2}."
    assert actual_f5 == expected_f5, f"Column f5 values are incorrect. Expected {expected_f5}, got {actual_f5}."