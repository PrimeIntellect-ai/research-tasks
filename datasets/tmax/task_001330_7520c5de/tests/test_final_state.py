# test_final_state.py
import os
import csv
import pytest

def test_results_csv_exists_and_metric():
    results_path = "/home/user/results.csv"
    assert os.path.exists(results_path), f"File {results_path} does not exist."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    try:
        with open(results_path, "r") as f:
            reader = csv.reader(f)
            data = {row[0].strip(): float(row[1].strip()) for row in reader if len(row) >= 2}
    except Exception as e:
        pytest.fail(f"Failed to read or parse {results_path}: {e}")

    assert "P01" in data, "P01 not found in results.csv"
    assert "P10" in data, "P10 not found in results.csv"
    assert "LLR" in data, "LLR not found in results.csv"

    p01 = data["P01"]
    p10 = data["P10"]

    error = abs(p01 - 0.15) + abs(p10 - 0.25)

    assert error < 0.06, f"Metric error {error:.4f} is not < 0.06 (P01={p01}, P10={p10})"