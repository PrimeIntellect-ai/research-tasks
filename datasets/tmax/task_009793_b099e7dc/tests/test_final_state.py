# test_final_state.py

import os
import pytest
from collections import defaultdict

def test_c_program_exists():
    """Check that the C program source file exists."""
    assert os.path.isfile("/home/user/analyze_backups.c"), "The C program file /home/user/analyze_backups.c is missing."

def test_output_file_exists():
    """Check that the output text file exists."""
    assert os.path.isfile("/home/user/critical_backups.txt"), "The output file /home/user/critical_backups.txt is missing."

def test_output_file_content():
    """Verify the content of the output file matches the expected top 3 databases."""
    csv_path = "/home/user/backup_deps.csv"
    assert os.path.isfile(csv_path), "The input CSV file is missing."

    # Recompute the expected truth
    out_degrees = defaultdict(int)
    with open(csv_path, "r") as f:
        lines = f.read().strip().splitlines()
        if lines:
            # Skip header
            for line in lines[1:]:
                parts = line.split(',')
                if len(parts) >= 1:
                    source_db = parts[0].strip()
                    out_degrees[source_db] += 1

    # Sort by count descending, then by name ascending
    sorted_dbs = sorted(out_degrees.items(), key=lambda x: (-x[1], x[0]))

    expected_lines = [f"{db}: {count}" for db, count in sorted_dbs[:3]]
    expected_content = "\n".join(expected_lines)

    with open("/home/user/critical_backups.txt", "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The contents of /home/user/critical_backups.txt are incorrect.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )