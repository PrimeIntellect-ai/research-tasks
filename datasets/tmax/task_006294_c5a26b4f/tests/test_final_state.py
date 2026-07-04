# test_final_state.py

import os
import re
import pytest

def test_go_program_exists():
    """Check that the Go program was created."""
    go_file = "/home/user/tokenize_dataset.go"
    assert os.path.isfile(go_file), f"Go program {go_file} is missing."

def test_experiments_csv_content():
    """Check that experiments.csv contains the correct computed metrics."""
    raw_data_dir = "/home/user/raw_data"
    assert os.path.isdir(raw_data_dir), f"Directory {raw_data_dir} is missing."

    txt_files = [f for f in os.listdir(raw_data_dir) if f.endswith(".txt")]
    total_files = len(txt_files)

    all_tokens = []
    for filename in txt_files:
        filepath = os.path.join(raw_data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().lower()
            tokens = re.findall(r'[a-z]+', content)
            all_tokens.extend(tokens)

    total_tokens = len(all_tokens)
    unique_tokens = len(set(all_tokens))

    expected_line = f"Run1,{total_files},{total_tokens},{unique_tokens}"

    csv_file = "/home/user/experiments.csv"
    assert os.path.isfile(csv_file), f"File {csv_file} was not created."

    with open(csv_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines, f"File {csv_file} is empty."

    # Check if the expected line is in the CSV (it should be the last appended line, or the only line)
    assert expected_line in lines, f"Expected line '{expected_line}' not found in {csv_file}. Found: {lines}"