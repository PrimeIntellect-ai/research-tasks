# test_final_state.py

import os
import tarfile
import pytest

def test_summary_txt_contents():
    """Test that summary.txt contains the correct sorted filenames."""
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"File {summary_path} does not exist."

    with open(summary_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_files = ["bin_143500.dat", "bin_144500.dat"]
    assert lines == expected_files, f"Contents of {summary_path} are incorrect. Expected {expected_files}, got {lines}."

def test_anomalies_backup_contents():
    """Test that anomalies_backup.tar.gz contains exactly the right files at the root level."""
    backup_path = "/home/user/anomalies_backup.tar.gz"
    assert os.path.isfile(backup_path), f"File {backup_path} does not exist."
    assert tarfile.is_tarfile(backup_path), f"{backup_path} is not a valid tar archive."

    with tarfile.open(backup_path, "r:gz") as tar:
        members = tar.getnames()

    expected_files = ["bin_143500.dat", "bin_144500.dat"]

    # Check that it contains exactly the expected files
    assert sorted(members) == sorted(expected_files), (
        f"Archive {backup_path} contents are incorrect. "
        f"Expected {sorted(expected_files)}, got {sorted(members)}."
    )