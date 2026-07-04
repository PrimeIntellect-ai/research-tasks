# test_final_state.py

import os
import pytest

def test_clean_users_csv_exists_and_content():
    output_file = "/home/user/clean_users.csv"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist. Did you run your C program?"
    assert os.path.isfile(output_file), f"{output_file} should be a file."

    expected_content = """BØB,2023-12-01T08:12:00Z,SYSTEM FAILURE IMMINENT
ZØE,2023-12-01T08:30:00Z,HéLLO WøRLD
alice,2023-12-01T08:25:00Z,WAIT, MY CAFé SPILLED!
charlie,2023-12-01T08:15:30Z,NEVERMIND, IT WORKS NOW.
dæmon,2023-12-01T08:20:00Z,RESTARTING SERVICES..."""

    with open(output_file, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    # Split into lines for better diffing in pytest
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        "The content of clean_users.csv does not match the expected output. "
        "Check your parsing, deduplication, normalization, and sorting logic."
    )