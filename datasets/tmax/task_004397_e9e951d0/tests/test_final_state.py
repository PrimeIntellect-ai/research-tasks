# test_final_state.py

import os
import hashlib
import pytest

def test_predictions_csv_content():
    path = "/home/user/predictions.csv"
    assert os.path.isfile(path), f"Missing predictions file: {path}"

    with open(path, 'r') as f:
        content = f.read()

    expected_content = "1,24\n2,27.9\n3,23.6\n"
    # Allow for missing trailing newline if the user didn't include it, but the standard output usually has it.
    # Let's check stripped lines to be robust, but also we need to check the exact hash later.
    lines = [line.strip() for line in content.strip().split('\n')]
    expected_lines = ["1,24", "2,27.9", "3,23.6"]

    assert lines == expected_lines, f"predictions.csv content is incorrect. Expected {expected_lines}, got {lines}"

def test_pipeline_hash_file():
    hash_path = "/home/user/pipeline_hash.txt"
    pred_path = "/home/user/predictions.csv"

    assert os.path.isfile(hash_path), f"Missing hash file: {hash_path}"
    assert os.path.isfile(pred_path), f"Missing predictions file: {pred_path}"

    with open(hash_path, 'r') as f:
        actual_hash = f.read().strip()

    with open(pred_path, 'rb') as f:
        pred_bytes = f.read()

    expected_hash = hashlib.sha256(pred_bytes).hexdigest()

    assert actual_hash == expected_hash, f"Hash in {hash_path} ({actual_hash}) does not match the actual sha256 hash of {pred_path} ({expected_hash})"

def test_pipeline_hash_exact():
    # To strictly enforce the expected output format including newlines
    hash_path = "/home/user/pipeline_hash.txt"
    assert os.path.isfile(hash_path), f"Missing hash file: {hash_path}"

    with open(hash_path, 'r') as f:
        actual_hash = f.read().strip()

    # The expected hash of "1,24\n2,27.9\n3,23.6\n"
    expected_hash = "165a250325f6e812f8a846f48037f9e0f6cba9c4a8cfba94b0d0c3546a1dfc3a"

    assert actual_hash == expected_hash, f"The hash value is incorrect. Expected {expected_hash}, got {actual_hash}"