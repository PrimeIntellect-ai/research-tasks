# test_final_state.py

import os
import glob
import subprocess
import tempfile
import pytest

def test_clean_extracted_csv():
    """Verify that the clean_extracted.csv file exists and contains valid data."""
    file_path = "/home/user/clean_extracted.csv"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"{file_path} is empty."

    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        assert len(parts) == 2, f"Invalid CSV format in {file_path}: expected 2 columns, got {len(parts)} in line '{line}'"
        try:
            ts = float(parts[0])
            size = float(parts[1])
        except ValueError:
            pytest.fail(f"Values in {file_path} are not valid floats: {line}")

        assert size >= 0, f"Negative size found in {file_path}: {line}"

def test_go_filter_clean_corpus():
    """Verify that the Go filter accepts all clean corpus files."""
    filter_script = "/home/user/filter.go"
    assert os.path.isfile(filter_script), f"Go filter script missing: {filter_script}"

    clean_files = glob.glob("/app/corpus/clean/*.csv")
    assert len(clean_files) > 0, "No clean corpus files found in /app/corpus/clean/"

    failed_files = []
    for f in clean_files:
        with tempfile.NamedTemporaryFile(suffix=".csv") as tmp:
            res = subprocess.run(
                ["go", "run", filter_script, f, tmp.name],
                capture_output=True,
                text=True
            )
            if res.returncode != 0:
                failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified or rejected: {failed_files}"

def test_go_filter_evil_corpus():
    """Verify that the Go filter rejects all evil corpus files."""
    filter_script = "/home/user/filter.go"
    assert os.path.isfile(filter_script), f"Go filter script missing: {filter_script}"

    evil_files = glob.glob("/app/corpus/evil/*.csv")
    assert len(evil_files) > 0, "No evil corpus files found in /app/corpus/evil/"

    failed_files = []
    for f in evil_files:
        with tempfile.NamedTemporaryFile(suffix=".csv") as tmp:
            res = subprocess.run(
                ["go", "run", filter_script, f, tmp.name],
                capture_output=True,
                text=True
            )
            if res.returncode == 0:
                failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {failed_files}"