# test_final_state.py

import os
import pytest

INCOMING_DIR = "/home/user/incoming"
OUTPUT_FILE = "/home/user/processed_dev01.csv"

def test_deduplication_completed():
    """Check that duplicate file C.dat was deleted and others kept."""
    expected_files = ["A.dat", "B.dat", "D.dat"]
    for f in expected_files:
        filepath = os.path.join(INCOMING_DIR, f)
        assert os.path.isfile(filepath), f"Expected file {filepath} to exist, but it is missing."

    deleted_file = os.path.join(INCOMING_DIR, "C.dat")
    assert not os.path.exists(deleted_file), f"Duplicate file {deleted_file} was not deleted."

def test_output_file_exists():
    """Check that the final output file was created."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} was not created."

def test_output_file_contents():
    """Check that the output file contains the correctly processed and gap-filled data."""
    expected_content = [
        "0,20",
        "1,20",
        "2,18",
        "3,18",
        "4,25"
    ]

    with open(OUTPUT_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_content, (
        f"Contents of {OUTPUT_FILE} do not match expected output.\n"
        f"Expected: {expected_content}\n"
        f"Got: {lines}"
    )