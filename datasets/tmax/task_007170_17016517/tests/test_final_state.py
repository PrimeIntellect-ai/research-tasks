# test_final_state.py
import os
import csv

def test_predictions_csv_exists():
    path = "/home/user/predictions.csv"
    assert os.path.exists(path), f"{path} was not found."
    assert os.path.isfile(path), f"{path} is not a file."

def test_benchmark_txt_exists():
    path = "/home/user/benchmark.txt"
    assert os.path.exists(path), f"{path} was not found."
    assert os.path.isfile(path), f"{path} is not a file."

def test_predictions_csv_content():
    path = "/home/user/predictions.csv"
    if not os.path.exists(path):
        return # Handled by previous test

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 1, "predictions.csv does not contain any data rows."

    header = rows[0]
    expected_header = ['machine_id', 'pc1', 'pc2', 'pc3', 'prediction']
    assert header == expected_header, f"Columns mismatch. Expected {expected_header}, got {header}."

    data_rows = rows[1:]

    # Check that machine_id does not contain decimals
    for i, row in enumerate(data_rows):
        machine_id = row[0]
        assert "." not in machine_id, f"machine_id at row {i} contains decimals: '{machine_id}'. It was not properly cast to int."

    # Check that missing value was imputed with 999 at index 150
    if len(data_rows) > 150:
        assert data_rows[150][0] == '999', f"Missing value at row 150 was not correctly imputed with 999. Found '{data_rows[150][0]}'."

def test_benchmark_txt_content():
    path = "/home/user/benchmark.txt"
    if not os.path.exists(path):
        return # Handled by previous test

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        raise AssertionError(f"benchmark.txt does not contain a valid float. Found: '{content}'")

    assert val >= 0, f"Benchmark value must be positive, got {val}."