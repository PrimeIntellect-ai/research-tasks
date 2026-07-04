# test_final_state.py

import os
import pytest

DATASET_DIR = "/home/user/dataset"
SUMMARY_LOG = "/home/user/summary.log"

EXPECTED_FILES = [
    "A1B2C3D4.dat",
    "F9E8D7C6.dat",
    "MNBVCXZA.dat",
    "Q1W2E3R4.dat",
    "ZZ99YY88.dat"
]

def test_no_raw_data_files():
    """Ensure original raw_data_*.dat files no longer exist."""
    assert os.path.isdir(DATASET_DIR), f"Directory {DATASET_DIR} does not exist."
    files = os.listdir(DATASET_DIR)
    raw_files = [f for f in files if f.startswith("raw_data_") and f.endswith(".dat")]
    assert len(raw_files) == 0, f"Original raw_data files still exist: {raw_files}"

def test_renamed_files_exist():
    """Ensure the files are renamed to their experiment IDs."""
    assert os.path.isdir(DATASET_DIR), f"Directory {DATASET_DIR} does not exist."
    files = os.listdir(DATASET_DIR)
    dat_files = [f for f in files if f.endswith(".dat")]

    assert set(dat_files) == set(EXPECTED_FILES), (
        f"Expected .dat files {EXPECTED_FILES}, but found {dat_files}"
    )

@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_cleaned_headers(filename):
    """Ensure the first 10 lines were removed and exactly 9,990 lines remain."""
    filepath = os.path.join(DATASET_DIR, filename)
    assert os.path.isfile(filepath), f"Expected file {filepath} is missing."

    with open(filepath, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 9990, f"File {filename} should have exactly 9,990 lines, but has {len(lines)}."
    assert lines[0].startswith("1234567890, "), f"First line of {filename} does not look like data. Headers might not be fully removed."
    assert "JUNK HEADER LINE" not in lines[0], f"First line of {filename} still contains header junk."

def test_summary_log():
    """Ensure summary.log contains the sorted list of new filenames."""
    assert os.path.isfile(SUMMARY_LOG), f"Summary log {SUMMARY_LOG} does not exist."

    with open(SUMMARY_LOG, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_sorted = sorted(EXPECTED_FILES)
    assert lines == expected_sorted, (
        f"Summary log contents do not match expected sorted filenames.\n"
        f"Expected: {expected_sorted}\n"
        f"Found: {lines}"
    )