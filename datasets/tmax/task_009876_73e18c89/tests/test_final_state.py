# test_final_state.py

import os
import csv
import ast
import pytest

def test_script_exists_and_uses_fcntl():
    script_path = "/home/user/curate_artifacts.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "fcntl.flock" in content or "fcntl.lockf" in content, (
        "Script does not contain 'fcntl.flock' or 'fcntl.lockf' for file locking."
    )

def test_csv_output_correctness():
    csv_path = "/home/user/artifact_repo/valid_inventory.csv"
    assert os.path.isfile(csv_path), f"Output CSV {csv_path} does not exist."

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."

    # Check header
    assert rows[0] == ["ArtifactID", "ResolvedPath", "Checksum"], (
        f"CSV header is incorrect. Got {rows[0]}"
    )

    # Expected data rows based on the logic:
    # pkg-101 is staged and valid.
    # pkg-102 is staged but in a symlink loop.
    # pkg-103 is staged and valid.
    # pkg-104 is archived (skip).
    # pkg-105 is staged and valid.
    expected_rows = [
        ["pkg-101", "/home/user/artifact_repo/binaries/v1/core.bin", "a1b2c3d4"],
        ["pkg-103", "/home/user/artifact_repo/binaries/valid_pkg.bin", "12345678"],
        ["pkg-105", "/home/user/artifact_repo/binaries/v2/util.bin", "87654321"],
    ]

    assert len(rows) - 1 == len(expected_rows), (
        f"Expected {len(expected_rows)} data rows, but got {len(rows) - 1}."
    )

    for i, expected in enumerate(expected_rows):
        actual = rows[i+1]
        assert actual == expected, (
            f"Row {i+1} incorrect. Expected {expected}, got {actual}"
        )