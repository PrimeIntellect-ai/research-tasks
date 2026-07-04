# test_final_state.py

import os
import csv

def test_ci_results_file():
    ci_file = "/home/user/ci_results.csv"
    assert os.path.isfile(ci_file), f"Expected output file {ci_file} is missing."

    with open(ci_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 3, f"Expected exactly 3 rows in {ci_file} (1 header + 2 data rows), found {len(rows)}."

    header = rows[0]
    assert header == ["group", "mean", "lower_bound", "upper_bound"], f"Incorrect header in {ci_file}: {header}"

    data_rows = rows[1:]

    # Create a dictionary for easier checking
    results = {row[0]: row[1:] for row in data_rows if len(row) == 4}

    assert "Positive" in results, "Missing 'Positive' group in ci_results.csv"
    assert "Negative" in results, "Missing 'Negative' group in ci_results.csv"

    pos_mean, pos_lower, pos_upper = results["Positive"]
    assert pos_mean == "174.100", f"Expected Positive mean to be '174.100', got {pos_mean}"
    assert pos_lower == "104.189", f"Expected Positive lower_bound to be '104.189', got {pos_lower}"
    assert pos_upper == "244.011", f"Expected Positive upper_bound to be '244.011', got {pos_upper}"

    neg_mean, neg_lower, neg_upper = results["Negative"]
    assert neg_mean == "65.000", f"Expected Negative mean to be '65.000', got {neg_mean}"
    assert neg_lower == "48.026", f"Expected Negative lower_bound to be '48.026', got {neg_lower}"
    assert neg_upper == "81.974", f"Expected Negative upper_bound to be '81.974', got {neg_upper}"

def test_model_results_file():
    model_file = "/home/user/model_results.txt"
    assert os.path.isfile(model_file), f"Expected output file {model_file} is missing."

    with open(model_file, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) >= 2, f"Expected at least 2 lines in {model_file}, found {len(content)}."

    slope_line = None
    intercept_line = None

    for line in content:
        if line.startswith("Slope:"):
            slope_line = line
        elif line.startswith("Intercept:"):
            intercept_line = line

    assert slope_line is not None, "Missing 'Slope:' line in model_results.txt"
    assert intercept_line is not None, "Missing 'Intercept:' line in model_results.txt"

    slope_val = slope_line.split(":")[1].strip()
    intercept_val = intercept_line.split(":")[1].strip()

    assert slope_val == "0.016", f"Expected Slope to be '0.016', got '{slope_val}'"
    assert intercept_val == "1.443", f"Expected Intercept to be '1.443', got '{intercept_val}'"