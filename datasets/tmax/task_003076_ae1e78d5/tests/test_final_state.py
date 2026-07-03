# test_final_state.py

import os
import pytest

def test_test_result_log():
    log_path = "/home/user/test_result.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. The testing script may not have run."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "REPRODUCIBILITY_PASS", f"Expected 'REPRODUCIBILITY_PASS' in {log_path}, but got '{content}'."

def test_aggregated_csv_batch_b():
    agg_path = "/home/user/processed/aggregated.csv"
    assert os.path.isfile(agg_path), f"File {agg_path} does not exist. The pipeline may not have produced the aggregated output."

    with open(agg_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "category,total_revenue",
        "Electronics,200.00",
        "Food,50.00"
    ]

    assert lines == expected_lines, f"Contents of {agg_path} do not match the expected output for batch_B.csv. Got: {lines}"

def test_invalid_ids_txt_batch_b():
    invalid_path = "/home/user/processed/invalid_ids.txt"
    assert os.path.isfile(invalid_path), f"File {invalid_path} does not exist. The pipeline may not have produced the invalid IDs output."

    with open(invalid_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = {
        "V1V2V3V4",
        "B1B2B3B4",
        "C1C2C3C4",
        "E1E2E3E4"
    }

    actual_ids = set(lines)

    assert len(lines) == 4, f"Expected exactly 4 lines in {invalid_path}, but got {len(lines)}."
    assert actual_ids == expected_ids, f"Contents of {invalid_path} do not match the expected invalid IDs for batch_B.csv. Got: {actual_ids}"