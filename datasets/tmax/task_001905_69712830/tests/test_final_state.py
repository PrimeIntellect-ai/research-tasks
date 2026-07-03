# test_final_state.py

import os
import csv
import re
import pytest

PIPELINE_DIR = "/home/user/ml_pipeline"
MAIN_CPP = os.path.join(PIPELINE_DIR, "main.cpp")
RESULTS_CSV = os.path.join(PIPELINE_DIR, "benchmark_results.csv")

def test_results_csv_exists():
    assert os.path.isfile(RESULTS_CSV), f"Expected results file {RESULTS_CSV} does not exist."

def test_results_csv_format_and_content():
    assert os.path.isfile(RESULTS_CSV), "Results CSV is missing."

    with open(RESULTS_CSV, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Results CSV is empty."

    header = rows[0]
    expected_header = ["alpha", "cv_mse", "avg_inference_time_us"]
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected exactly 3 rows of data, found {len(data_rows)}."

    expected_alphas = ["0.1", "1.0", "10.0"]
    actual_alphas = []

    for i, row in enumerate(data_rows):
        assert len(row) == 3, f"Row {i+1} does not have exactly 3 columns: {row}"
        alpha_str, cv_mse_str, time_str = row

        # Check alpha
        actual_alphas.append(alpha_str)

        # Check cv_mse is a float and has 3 decimal places (or at least parses as float)
        try:
            cv_mse = float(cv_mse_str)
        except ValueError:
            pytest.fail(f"cv_mse value '{cv_mse_str}' in row {i+1} is not a valid float.")

        # Check avg_inference_time_us is numeric
        try:
            time_val = float(time_str)
            assert time_val >= 0, f"Inference time cannot be negative, got {time_val}"
        except ValueError:
            pytest.fail(f"avg_inference_time_us value '{time_str}' in row {i+1} is not valid.")

    # Check if alphas match (ignoring exact formatting like 0.1 vs 0.10, but string match is safer if they follow instructions)
    actual_alphas_float = [float(a) for a in actual_alphas]
    expected_alphas_float = [0.1, 1.0, 10.0]
    assert actual_alphas_float == expected_alphas_float, f"Expected alphas {expected_alphas_float}, got {actual_alphas_float}."

def test_data_leak_fixed_in_main_cpp():
    assert os.path.isfile(MAIN_CPP), f"Source file {MAIN_CPP} is missing."

    with open(MAIN_CPP, "r") as f:
        content = f.read()

    # The original buggy code calls scale_data_globally(data); before the alpha loop.
    # We should ensure that global scaling before splitting is removed.
    # A simple heuristic: scale_data_globally(data) should not be present in its original form,
    # or at least the data is scaled per fold.

    # Check if chrono is included for benchmarking
    assert "<chrono>" in content, "Expected <chrono> to be included for inference benchmarking."

    # Check that scale_data_globally(data) is not called directly on the full dataset
    # We can check if the string "scale_data_globally(data);" is removed or modified.
    buggy_call_pattern = r"scale_data_globally\s*\(\s*data\s*\)\s*;"
    assert not re.search(buggy_call_pattern, content), "The data leak appears to be unfixed: global scaling is still called on the full dataset."