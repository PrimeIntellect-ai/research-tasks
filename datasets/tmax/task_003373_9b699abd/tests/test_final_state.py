# test_final_state.py

import os
import csv
import math
import pytest

def test_datamash_installed():
    datamash_path = "/home/user/local/bin/datamash"
    assert os.path.isfile(datamash_path), f"{datamash_path} does not exist. Did you install datamash?"
    assert os.access(datamash_path, os.X_OK), f"{datamash_path} is not executable."

def test_process_data_script_exists():
    script_path = "/home/user/process_data.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK) or True, "Script should ideally be executable."

def test_cleaned_data_tsv():
    cleaned_path = "/home/user/cleaned_data.tsv"
    assert os.path.isfile(cleaned_path), f"Cleaned data file {cleaned_path} does not exist."

    with open(cleaned_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 8, f"Expected 8 valid rows in cleaned_data.tsv, found {len(lines)}."

    expected_rows = {
        "Exp1\t2022-12-31\tAlpha\t12.50",
        "Exp2\t2023-01-01\tBeta\t10.00",
        "Exp3\t2023-01-02\tAlpha\t5.25",
        "Exp5\t2023-01-04\tBeta\t20.00",
        "Exp6\t2023-10-15\tAlpha\t3.25",
        "Exp7\t2023-10-16\tBeta\t15.50",
        "Exp8\t2023-10-17\tGamma\t100.00",
        "Exp10\t2023-10-19\tGamma\t200.50"
    }

    # We will check if the normalized versions of the rows match
    actual_rows = set()
    for line in lines:
        parts = line.split("\t")
        assert len(parts) == 4, f"Row does not have 4 tab-separated columns: {line}"
        # Normalize the float to 2 decimal places for comparison
        try:
            val = float(parts[3])
            parts[3] = f"{val:.2f}"
        except ValueError:
            pytest.fail(f"Value column contains non-float: {parts[3]} in row {line}")
        actual_rows.add("\t".join(parts))

    for expected in expected_rows:
        assert expected in actual_rows, f"Expected row '{expected}' not found in cleaned_data.tsv."

def test_summary_csv():
    summary_path = "/home/user/results/summary.csv"
    assert os.path.isfile(summary_path), f"Summary CSV {summary_path} does not exist."

    with open(summary_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Summary CSV is empty."

    header = rows[0]
    assert header == ["Category", "Total", "Average"], f"Incorrect header in summary.csv: {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected 3 data rows in summary.csv, found {len(data_rows)}."

    # Expected values
    expected_data = {
        "Alpha": {"Total": 21.0, "Average": 7.0},
        "Beta": {"Total": 45.5, "Average": 15.166666666667},
        "Gamma": {"Total": 300.5, "Average": 150.25}
    }

    categories_found = set()
    for row in data_rows:
        assert len(row) == 3, f"Row does not have 3 columns: {row}"
        category, total_str, avg_str = row
        categories_found.add(category)

        assert category in expected_data, f"Unexpected category '{category}' found."

        try:
            total = float(total_str)
            avg = float(avg_str)
        except ValueError:
            pytest.fail(f"Non-numeric value in total/average for category {category}: {total_str}, {avg_str}")

        expected_total = expected_data[category]["Total"]
        expected_avg = expected_data[category]["Average"]

        assert math.isclose(total, expected_total, rel_tol=1e-5), f"Incorrect total for {category}: expected {expected_total}, got {total}"
        assert math.isclose(avg, expected_avg, rel_tol=1e-2), f"Incorrect average for {category}: expected {expected_avg}, got {avg}"

    assert categories_found == {"Alpha", "Beta", "Gamma"}, "Not all expected categories were found in summary.csv."