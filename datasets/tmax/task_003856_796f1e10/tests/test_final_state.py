# test_final_state.py

import os
import pytest

FINAL_METRIC_PATH = "/home/user/final_metric.txt"

def test_final_metric_exists():
    assert os.path.isfile(FINAL_METRIC_PATH), f"Expected output file {FINAL_METRIC_PATH} does not exist."

def test_final_metric_content():
    assert os.path.isfile(FINAL_METRIC_PATH), f"Output file {FINAL_METRIC_PATH} is missing."

    with open(FINAL_METRIC_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # The sum of 1 to 50 is 50 * 51 / 2 = 1275
    expected_sum = "1275"

    assert content == expected_sum, f"Expected final metric to be '{expected_sum}', but got '{content}'."