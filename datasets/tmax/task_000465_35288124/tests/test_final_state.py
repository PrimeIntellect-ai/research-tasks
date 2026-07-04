# test_final_state.py
import os

def test_experiment_log_exists():
    filepath = "/home/user/experiment_log.tsv"
    assert os.path.isfile(filepath), f"Expected output file {filepath} is missing. Did the script run and create it?"

def test_experiment_log_content():
    filepath = "/home/user/experiment_log.tsv"
    assert os.path.isfile(filepath), f"Expected output file {filepath} is missing."

    expected_lines = [
        "id\tv1\tv2\tvalid",
        "doc1\t0.00\t1.00\ttrue",
        "doc2\t0.00\t0.00\ttrue",
        "doc3\t5.00\t-5.00\tfalse",
        "doc4\t0.00\t0.00\ttrue",
        "doc5\t0.00\t0.00\ttrue"
    ]

    with open(filepath, "r") as f:
        actual_lines = f.read().strip().split("\n")

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in {filepath}, but found {len(actual_lines)}"
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} in {filepath} does not match expected output.\n"
            f"Expected: {repr(expected)}\n"
            f"Actual:   {repr(actual)}"
        )