# test_final_state.py

import os
import csv
import math

def test_files_exist():
    assert os.path.isfile("/home/user/prepare_data.py"), "/home/user/prepare_data.py is missing."
    assert os.path.isfile("/home/user/run_pipeline.sh"), "/home/user/run_pipeline.sh is missing."
    assert os.path.isfile("/home/user/training_data.csv"), "/home/user/training_data.csv is missing."

def test_pipeline_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.access(script_path, os.X_OK), f"{script_path} must be executable."

def test_csv_output():
    csv_path = "/home/user/training_data.csv"

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."

    header = rows[0]
    expected_header = ["sequence", "L", "GC", "x"]
    assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

    expected_data = [
        {"sequence": "CGTAGCTAGC", "L": 10, "GC": 0.6000, "x": 21.0333},
        {"sequence": "ATCGATCGAT", "L": 10, "GC": 0.4000, "x": 21.5714},
        {"sequence": "CTAGCATCGA", "L": 10, "GC": 0.5000, "x": 21.3283}
    ]

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} rows, got {len(data_rows)}"

    for i, (row, expected) in enumerate(zip(data_rows, expected_data)):
        assert len(row) == 4, f"Row {i+1} does not have 4 columns."

        seq, l_str, gc_str, x_str = row
        assert seq == expected["sequence"], f"Row {i+1} sequence mismatch. Expected {expected['sequence']}, got {seq}"

        try:
            l_val = int(l_str)
            gc_val = float(gc_str)
            x_val = float(x_str)
        except ValueError:
            assert False, f"Row {i+1} contains invalid numeric values: {row}"

        assert l_val == expected["L"], f"Row {i+1} L mismatch. Expected {expected['L']}, got {l_val}"
        assert math.isclose(gc_val, expected["GC"], abs_tol=1e-4), f"Row {i+1} GC mismatch. Expected {expected['GC']}, got {gc_val}"
        assert math.isclose(x_val, expected["x"], abs_tol=1e-4), f"Row {i+1} x mismatch. Expected {expected['x']}, got {x_val}"