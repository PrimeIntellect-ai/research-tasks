import os
import csv
import math
import pytest

def test_r_value_file():
    """Test that r_value.txt exists and contains the correct r value."""
    r_file = "/home/user/r_value.txt"
    assert os.path.isfile(r_file), f"{r_file} is missing."
    with open(r_file, "r") as f:
        content = f.read().strip()

    # Expected r is 0.42
    assert content == "0.42", f"Expected r value 0.42, but got {content}"

def test_results_csv_file():
    """Test that results.csv exists and contains expected values."""
    csv_file = "/home/user/results.csv"
    assert os.path.isfile(csv_file), f"{csv_file} is missing."

    expected_actuals = [100, 149, 222, 330, 485, 706, 1014, 1432, 1980, 2680]
    expected_predicteds = [100.00, 150.31, 224.22, 331.02, 483.17, 695.53, 986.32, 1375.05, 1882.26, 2522.61]

    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["Day", "Actual", "Predicted"], f"Incorrect CSV header: {header}"

        rows = list(reader)
        assert len(rows) == 10, f"Expected 10 rows of data, found {len(rows)}"

        for i, row in enumerate(rows):
            assert len(row) == 3, f"Row {i+1} does not have 3 columns"
            day, actual, predicted = row
            assert int(day) == i + 1, f"Expected Day {i+1}, got {day}"
            assert int(actual) == expected_actuals[i], f"Expected Actual {expected_actuals[i]}, got {actual}"
            assert math.isclose(float(predicted), expected_predicteds[i], abs_tol=0.05), f"Expected Predicted {expected_predicteds[i]}, got {predicted}"

def test_plot_file():
    """Test that fit_plot.png exists."""
    plot_file = "/home/user/fit_plot.png"
    assert os.path.isfile(plot_file), f"{plot_file} is missing."
    assert os.path.getsize(plot_file) > 0, f"{plot_file} is empty."