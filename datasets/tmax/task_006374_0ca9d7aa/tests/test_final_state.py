# test_final_state.py

import os
import json
import pytest

DATA_FILE = "/home/user/data.csv"
BOOTSTRAP_FILE = "/home/user/bootstrap.csv"
OUTPUT_PNG = "/home/user/output.png"
METRICS_JSON = "/home/user/metrics.json"

def test_bootstrap_csv_exists_and_size():
    """Check that bootstrap.csv exists and has the same number of lines as data.csv."""
    assert os.path.isfile(BOOTSTRAP_FILE), f"{BOOTSTRAP_FILE} does not exist."

    with open(DATA_FILE, 'r') as f:
        data_lines = f.readlines()

    with open(BOOTSTRAP_FILE, 'r') as f:
        bootstrap_lines = f.readlines()

    assert len(bootstrap_lines) == len(data_lines), \
        f"Expected {len(data_lines)} lines in {BOOTSTRAP_FILE}, found {len(bootstrap_lines)}."

def test_bootstrap_csv_content():
    """Check that all lines in bootstrap.csv are sampled from data.csv."""
    with open(DATA_FILE, 'r') as f:
        data_lines = set(f.readlines())

    with open(BOOTSTRAP_FILE, 'r') as f:
        bootstrap_lines = f.readlines()

    for i, line in enumerate(bootstrap_lines):
        assert line in data_lines, f"Line {i+1} in {BOOTSTRAP_FILE} is not from {DATA_FILE}: {line.strip()}"

def test_output_png_validity():
    """Check that output.png exists and is not a blank plot (size > 5000 bytes)."""
    assert os.path.isfile(OUTPUT_PNG), f"{OUTPUT_PNG} does not exist."

    file_size = os.path.getsize(OUTPUT_PNG)
    assert file_size > 5000, \
        f"{OUTPUT_PNG} is too small ({file_size} bytes). It appears to be a blank plot. Did you fix the matplotlib bug?"

def test_metrics_json_validity():
    """Check that metrics.json exists, is valid JSON, and contains 'mean_error'."""
    assert os.path.isfile(METRICS_JSON), f"{METRICS_JSON} does not exist."

    with open(METRICS_JSON, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{METRICS_JSON} is not a valid JSON file.")

    assert "mean_error" in metrics, f"'mean_error' key missing from {METRICS_JSON}."
    assert isinstance(metrics["mean_error"], (int, float)), "'mean_error' should be a number."