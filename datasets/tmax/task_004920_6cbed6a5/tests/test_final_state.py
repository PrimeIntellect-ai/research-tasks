# test_final_state.py

import os
import csv
import math
import pytest

def test_files_exist():
    """Test that all expected files are created."""
    expected_files = [
        "/home/user/etl.c",
        "/home/user/pipeline.sh",
        "/home/user/run_etl",
        "/home/user/clean_run1.tsv",
        "/home/user/clean_run2.tsv",
        "/home/user/z_stat.txt",
        "/home/user/run_log.txt"
    ]
    for file_path in expected_files:
        assert os.path.exists(file_path), f"Expected file {file_path} is missing."
        assert os.path.isfile(file_path), f"Path {file_path} is not a regular file."

def test_run_log_content():
    """Test that run_log.txt contains exactly 'Reproducible'."""
    with open("/home/user/run_log.txt", "r") as f:
        content = f.read().strip()
    assert content == "Reproducible", f"Expected 'Reproducible' in run_log.txt, but got '{content}'."

def test_clean_tsv_content():
    """Test that clean_run1.tsv and clean_run2.tsv match the expected filtered data."""
    raw_path = "/home/user/raw.tsv"
    clean1_path = "/home/user/clean_run1.tsv"
    clean2_path = "/home/user/clean_run2.tsv"

    expected_rows = []
    with open(raw_path, "r", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) < 4:
                continue
            rating = int(row[2])
            latency = float(row[3])
            if rating in [1, 2, 3, 4, 5] and 10.0 <= latency <= 5000.0:
                expected_rows.append(row)

    for clean_path in [clean1_path, clean2_path]:
        actual_rows = []
        with open(clean_path, "r", newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            actual_rows = list(reader)

        assert len(actual_rows) == len(expected_rows), f"Row count mismatch in {clean_path}. Expected {len(expected_rows)}, got {len(actual_rows)}."
        for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
            assert actual == expected, f"Row {i+1} mismatch in {clean_path}. Expected {expected}, got {actual}."

def test_z_stat_content():
    """Test that z_stat.txt contains the correct calculated Z-statistic."""
    raw_path = "/home/user/raw.tsv"

    g1 = []
    g2 = []
    with open(raw_path, "r", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) < 4:
                continue
            rating = int(row[2])
            latency = float(row[3])
            if rating in [1, 2, 3, 4, 5] and 10.0 <= latency <= 5000.0:
                if rating >= 4:
                    g1.append(latency)
                else:
                    g2.append(latency)

    n1 = len(g1)
    n2 = len(g2)

    mean1 = sum(g1) / n1 if n1 > 0 else 0
    mean2 = sum(g2) / n2 if n2 > 0 else 0

    var1 = sum((x - mean1) ** 2 for x in g1) / (n1 - 1) if n1 > 1 else 0
    var2 = sum((x - mean2) ** 2 for x in g2) / (n2 - 1) if n2 > 1 else 0

    z = abs(mean1 - mean2) / math.sqrt((var1 / n1) + (var2 / n2))
    expected_z = f"{z:.3f}"

    with open("/home/user/z_stat.txt", "r") as f:
        actual_z = f.read().strip()

    assert actual_z == expected_z, f"Expected Z-statistic {expected_z}, but got {actual_z} in z_stat.txt."