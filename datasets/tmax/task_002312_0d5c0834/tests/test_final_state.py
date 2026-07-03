# test_final_state.py
import os
import csv

def test_heavy_triangles_csv():
    csv_path = "/home/user/heavy_triangles.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist. Did you run your C program?"

    expected_rows = [
        ["node_id", "label", "out_degree"],
        ["1", "Alpha", "2"],
        ["2", "Bravo", "3"],
        ["3", "Charlie", "1"]
    ]

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        # Strip any trailing whitespace from rows and ignore empty lines
        actual_rows = [[cell.strip() for cell in row] for row in reader if row]

    assert actual_rows == expected_rows, f"CSV contents do not match expected.\nExpected: {expected_rows}\nActual: {actual_rows}"

def test_c_program_exists():
    c_path = "/home/user/process_graph.c"
    assert os.path.isfile(c_path), f"C source file {c_path} does not exist."