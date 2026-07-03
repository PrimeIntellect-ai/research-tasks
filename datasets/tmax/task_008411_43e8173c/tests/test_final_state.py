# test_final_state.py

import os
import csv
import math
import pytest

SUMMARY_FILE = "/home/user/experiments/summary.csv"
CPP_SOURCE = "/home/user/experiments/process_logs.cpp"
CPP_BIN = "/home/user/experiments/process_logs"

def test_summary_file_exists():
    """Check if the summary.csv file was generated."""
    assert os.path.isfile(SUMMARY_FILE), f"The file {SUMMARY_FILE} does not exist. Did the C++ program run successfully?"

def test_summary_csv_content():
    """Validate the contents, sorting, and formatting of summary.csv."""
    assert os.path.isfile(SUMMARY_FILE), "Summary file missing."

    with open(SUMMARY_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "summary.csv is empty."

    header = rows[0]
    expected_header = ["learning_rate", "batch_size", "mean_val_accuracy", "total_training_time", "mean_optimizer"]
    assert header == expected_header, f"Header is incorrect. Expected {expected_header}, got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 4, f"Expected 4 data rows, got {len(data_rows)}"

    expected_data = [
        (0.05, 128, 0.9000, 435, 0.6666666667),
        (0.01, 64, 0.8800, 105, 1.0000),
        (0.01, 32, 0.8550, 190, 0.5000),
        (0.001, 64, 0.8100, 230, 0.5000),
    ]

    for i, (row, expected) in enumerate(zip(data_rows, expected_data)):
        assert len(row) == 5, f"Row {i+1} does not have 5 columns: {row}"

        lr_str, bs_str, acc_str, time_str, opt_str = row
        exp_lr, exp_bs, exp_acc, exp_time, exp_opt = expected

        # Check float equivalence
        assert math.isclose(float(lr_str), exp_lr, rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1} learning_rate expected ~{exp_lr}, got {lr_str}"
        assert math.isclose(float(bs_str), exp_bs, rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1} batch_size expected ~{exp_bs}, got {bs_str}"
        assert math.isclose(float(acc_str), exp_acc, rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1} mean_val_accuracy expected ~{exp_acc}, got {acc_str}"
        assert math.isclose(float(time_str), exp_time, rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1} total_training_time expected ~{exp_time}, got {time_str}"
        assert math.isclose(float(opt_str), exp_opt, rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1} mean_optimizer expected ~{exp_opt}, got {opt_str}"

        # Check 4 decimal places formatting for floats
        # The prompt says "All floating-point numbers in the output CSV must be formatted to exactly 4 decimal places"
        # Since learning_rate, mean_val_accuracy, and mean_optimizer are definitely floats, check them.
        for val_str, col_name in [(lr_str, "learning_rate"), (acc_str, "mean_val_accuracy"), (opt_str, "mean_optimizer")]:
            if '.' in val_str:
                decimals = len(val_str.split('.')[1])
                assert decimals == 4, f"Column {col_name} in row {i+1} must have exactly 4 decimal places. Got {val_str}"

def test_cpp_files_exist():
    """Check if the C++ source and binary exist."""
    assert os.path.isfile(CPP_SOURCE), f"The C++ source file {CPP_SOURCE} does not exist."
    assert os.path.isfile(CPP_BIN), f"The compiled binary {CPP_BIN} does not exist."
    assert os.access(CPP_BIN, os.X_OK), f"The file {CPP_BIN} is not executable."