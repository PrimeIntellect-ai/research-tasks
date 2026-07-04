# test_final_state.py

import os
import subprocess
import csv
import io
import pytest

SCRIPT_PATH = "/home/user/analyze.sh"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def run_script(target_dataset):
    result = subprocess.run(
        ["bash", SCRIPT_PATH, target_dataset],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed for {target_dataset} with error:\n{result.stderr}"
    return result.stdout.strip()

def test_analyze_dataset_c():
    output = run_script("Dataset_C")

    reader = csv.reader(io.StringIO(output))
    rows = list(reader)

    assert len(rows) > 0, "Output is empty"

    header = rows[0]
    expected_header = ["dependent_name", "category", "depth", "category_rank"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    data_rows = rows[1:]
    # Convert to set of tuples for order-independent comparison
    data_set = {tuple(row) for row in data_rows}

    expected_data = {
        ("Dataset_B", "Genomics", "1", "1"),
        ("Dataset_A", "Genomics", "2", "2"),
        ("Dataset_E", "Genomics", "3", "3"),
        ("Dataset_F", "Proteomics", "2", "1"),
        ("Dataset_D", "Transcriptomics", "1", "1"),
        ("Dataset_G", "Transcriptomics", "3", "2")
    }

    assert data_set == expected_data, f"Expected data {expected_data}, got {data_set}"

def test_analyze_dataset_b():
    output = run_script("Dataset_B")

    reader = csv.reader(io.StringIO(output))
    rows = list(reader)

    assert len(rows) > 0, "Output is empty"

    header = rows[0]
    expected_header = ["dependent_name", "category", "depth", "category_rank"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    data_rows = rows[1:]
    data_set = {tuple(row) for row in data_rows}

    expected_data = {
        ("Dataset_A", "Genomics", "1", "1"),
        ("Dataset_E", "Genomics", "2", "2"),
        ("Dataset_F", "Proteomics", "1", "1"),
        ("Dataset_G", "Transcriptomics", "2", "1")
    }

    assert data_set == expected_data, f"Expected data {expected_data}, got {data_set}"