# test_final_state.py

import os
import csv
import pytest

WORKSPACE = "/home/user/workspace"
ARTIFACTS_DIR = os.path.join(WORKSPACE, "artifacts")
CURATED_DIR = os.path.join(WORKSPACE, "curated")
CSV_PATH = os.path.join(WORKSPACE, "curated_summary.csv")

def test_csv_summary_exists_and_correct():
    assert os.path.isfile(CSV_PATH), f"Summary CSV not found at {CSV_PATH}"

    with open(CSV_PATH, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty"

    # Check headers
    assert rows[0] == ["Project", "Version", "Filename", "Status"], f"Incorrect CSV headers: {rows[0]}"

    # Check data rows
    expected_data = [
        ["Alpha", "2.0.0", "alpha-2.0.0.zip", "WARNING"],
        ["Alpha", "1.0.0", "alpha-1.0.0.zip", "SUCCESS"],
        ["Beta", "1.0.0", "beta-1.0.0.zip", "SUCCESS"]
    ]

    assert rows[1:] == expected_data, f"CSV data rows do not match expected output. Got: {rows[1:]}"

def test_curated_directory_structure_and_hard_links():
    assert os.path.isdir(CURATED_DIR), f"Curated directory not found at {CURATED_DIR}"

    expected_files = [
        ("Alpha", "1.0.0", "alpha-1.0.0.zip"),
        ("Alpha", "2.0.0", "alpha-2.0.0.zip"),
        ("Beta", "1.0.0", "beta-1.0.0.zip")
    ]

    for project, version, filename in expected_files:
        curated_path = os.path.join(CURATED_DIR, project, version, filename)
        original_path = os.path.join(ARTIFACTS_DIR, filename)

        assert os.path.isfile(curated_path), f"Curated artifact not found at {curated_path}"

        # Check hard link (must share the same inode)
        curated_stat = os.stat(curated_path)
        original_stat = os.stat(original_path)

        assert curated_stat.st_ino == original_stat.st_ino, f"File {curated_path} is not a hard link to {original_path}"

def test_symlinks_for_latest_versions():
    expected_symlinks = [
        ("Alpha", "2.0.0"),
        ("Beta", "1.0.0")
    ]

    for project, latest_version in expected_symlinks:
        symlink_path = os.path.join(CURATED_DIR, project, "latest")

        assert os.path.islink(symlink_path), f"Symlink 'latest' not found for project {project} at {symlink_path}"

        target = os.readlink(symlink_path)

        # The target could be just "2.0.0" or an absolute path resolving to the same directory
        resolved_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
        expected_resolved = os.path.abspath(os.path.join(CURATED_DIR, project, latest_version))

        assert resolved_target == expected_resolved, f"Symlink for {project} does not point to the correct latest version directory. Points to {target}"

def test_discarded_artifacts_not_in_curated():
    # ART-004 (Beta 1.1.0) is corrupted, ART-005 (Gamma 1.0.0) FAILED.
    beta_bad_path = os.path.join(CURATED_DIR, "Beta", "1.1.0")
    gamma_path = os.path.join(CURATED_DIR, "Gamma")

    assert not os.path.exists(beta_bad_path), f"Corrupted artifact version directory should not exist: {beta_bad_path}"
    assert not os.path.exists(gamma_path), f"Failed artifact project directory should not exist: {gamma_path}"