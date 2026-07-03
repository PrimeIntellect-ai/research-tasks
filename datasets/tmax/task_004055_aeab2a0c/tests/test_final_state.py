# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_features_csv_exists():
    """Verify that the features.csv file was generated."""
    features_path = "/home/user/features.csv"
    assert os.path.isfile(features_path), f"Features CSV is missing at {features_path}"
    assert os.path.getsize(features_path) > 0, f"Features CSV at {features_path} is empty"

def test_sanitizer_script_exists():
    """Verify that the sanitizer script exists."""
    script_path = "/home/user/sanitizer.py"
    assert os.path.isfile(script_path), f"Sanitizer script is missing at {script_path}"

def test_sanitizer_clean_corpus():
    """Verify that the sanitizer accepts all clean CSVs."""
    script_path = "/home/user/sanitizer.py"
    clean_dir = "/app/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(clean_files) > 0, f"No CSV files found in clean corpus directory {clean_dir}"

    failed_files = []
    for csv_file in clean_files:
        result = subprocess.run(["python3", script_path, csv_file], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(csv_file))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {failed_files}"

def test_sanitizer_evil_corpus():
    """Verify that the sanitizer rejects all evil CSVs."""
    script_path = "/home/user/sanitizer.py"
    evil_dir = "/app/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(evil_files) > 0, f"No CSV files found in evil corpus directory {evil_dir}"

    failed_files = []
    for csv_file in evil_files:
        result = subprocess.run(["python3", script_path, csv_file], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(csv_file))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {failed_files}"