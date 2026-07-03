# test_final_state.py

import os
import pytest

def test_extracted_log_recall():
    log_path = "/home/user/extracted.log"

    assert os.path.exists(log_path), f"Expected output file not found at {log_path}."
    assert os.path.isfile(log_path), f"Path {log_path} exists but is not a file."

    expected = set([f"SECRET_PAYLOAD_{i}" for i in range(100)])

    try:
        with open(log_path, "r") as f:
            extracted = set([line.strip() for line in f if line.strip()])
    except Exception as e:
        pytest.fail(f"Failed to read {log_path}: {e}")

    correct = len(expected.intersection(extracted))
    recall = correct / len(expected)

    threshold = 0.95
    assert recall >= threshold, (
        f"Recall metric failed. Expected recall >= {threshold}, but got {recall:.2f}. "
        f"Correctly extracted {correct} out of {len(expected)} expected payloads."
    )

def test_extracted_log_contains_no_garbage():
    log_path = "/home/user/extracted.log"
    if not os.path.exists(log_path):
        pytest.skip("Log file not found, skipping garbage check.")

    expected = set([f"SECRET_PAYLOAD_{i}" for i in range(100)])

    with open(log_path, "r") as f:
        extracted = set([line.strip() for line in f if line.strip()])

    # Optional check to see if there are too many unexpected lines, though the task only strictly evaluates recall.
    # We will just ensure the file is reasonably sized and not filled with infinite loop garbage.
    assert len(extracted) <= 200, f"File contains too many lines ({len(extracted)}). Did the parser loop infinitely or extract garbage?"