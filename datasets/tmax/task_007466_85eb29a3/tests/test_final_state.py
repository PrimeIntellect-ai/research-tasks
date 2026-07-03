# test_final_state.py

import os
import pytest

def test_final_results_file():
    results_file = "/home/user/ticket_system/final_results.txt"
    assert os.path.isfile(results_file), f"The file {results_file} does not exist. Did you run the script and redirect the output?"

    with open(results_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_results = {
        "data/batch_1.txt: 6",
        "data/batch_2.txt: 6",
        "data/batch_3.txt: 14",
        "data/batch_4.txt: 6",
        "data/batch_5.txt: 6",
        "data/batch_6.txt: 6",
        "data/batch_7.txt: 21",
        "data/batch_8.txt: 6",
        "data/batch_9.txt: 6",
        "data/batch_10.txt: 6"
    }

    actual_results = set(lines)

    missing = expected_results - actual_results
    unexpected = actual_results - expected_results

    assert not missing, f"Missing expected results in {results_file}: {missing}"
    assert not unexpected, f"Unexpected results found in {results_file}: {unexpected}"
    assert len(lines) == 10, f"Expected exactly 10 lines in {results_file}, but found {len(lines)}"