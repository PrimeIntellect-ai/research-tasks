# test_final_state.py

import os
import re
import pytest

MASTER_INDEX_PATH = "/home/user/dataset/master_index.csv"
RAW_DIR = "/home/user/dataset/raw"

def test_master_index_exists():
    assert os.path.isfile(MASTER_INDEX_PATH), f"Expected output file {MASTER_INDEX_PATH} does not exist."

def test_master_index_line_count():
    with open(MASTER_INDEX_PATH, "r") as f:
        lines = f.readlines()

    assert len(lines) == 100, f"Expected exactly 100 lines in {MASTER_INDEX_PATH}, but got {len(lines)}."

def test_master_index_format_and_no_corruption():
    with open(MASTER_INDEX_PATH, "r") as f:
        lines = f.readlines()

    # Regex to ensure no interleaved/corrupted lines
    # Path should start with /home/user/dataset/raw/ and end with a 4-decimal float
    pattern = re.compile(r'^/home/user/dataset/raw/.*,[0-9]+\.[0-9]{4}\n?$')

    bad_lines = []
    for i, line in enumerate(lines):
        if not pattern.match(line):
            bad_lines.append((i + 1, line.strip()))

    assert not bad_lines, f"Found {len(bad_lines)} corrupted or incorrectly formatted lines (file locking likely failed). Examples: {bad_lines[:5]}"

def test_master_index_exact_contents():
    with open(MASTER_INDEX_PATH, "r") as f:
        lines = f.read().splitlines()

    results = {}
    for line in lines:
        parts = line.split(',')
        if len(parts) == 2:
            path, mean_str = parts
            results[path] = float(mean_str)

    # Calculate the expected sum of means
    # The setup script creates 100 files with values i from 0 to 99.
    total_sum = sum(results.values())

    # Check sum
    expected_sum = sum(range(100))
    assert abs(total_sum - expected_sum) < 1e-6, f"Expected sum of averages to be {expected_sum:.4f}, got {total_sum:.4f}"

    # Check that we have exactly 100 unique valid file paths
    assert len(results) == 100, f"Expected 100 unique file paths, got {len(results)}"

    for path in results:
        assert path.startswith(RAW_DIR), f"Path {path} does not start with {RAW_DIR}"
        assert path.endswith('.bin') or path.endswith('.tsv'), f"Path {path} does not end with .bin or .tsv"