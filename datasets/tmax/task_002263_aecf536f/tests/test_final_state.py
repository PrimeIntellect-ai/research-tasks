# test_final_state.py

import os
import tarfile
import csv
import pytest

def test_tarball_exists():
    tarball_path = "/home/user/incremental_backup.tar.gz"
    assert os.path.isfile(tarball_path), f"Tarball {tarball_path} does not exist. Did you create the archive?"

def test_tarball_contents():
    tarball_path = "/home/user/incremental_backup.tar.gz"
    assert os.path.isfile(tarball_path), "Tarball missing."

    with tarfile.open(tarball_path, "r:gz") as tar:
        members = tar.getnames()

        # Check that the tarball contains exactly the expected files at the root
        assert "DS_001.csv" in members, "DS_001.csv is missing from the tarball root."
        assert "DS_003.csv" in members, "DS_003.csv is missing from the tarball root."
        assert "DS_002.csv" not in members, "DS_002.csv should not be in the tarball (it had FAILED status)."

        # Check that no absolute paths or backup_staging directory are in the tarball
        for member in members:
            assert not member.startswith("/"), f"Archive contains absolute path: {member}"
            assert "backup_staging" not in member, f"Archive contains 'backup_staging' directory structure: {member}"

def test_csv_contents():
    tarball_path = "/home/user/incremental_backup.tar.gz"
    assert os.path.isfile(tarball_path), "Tarball missing."

    with tarfile.open(tarball_path, "r:gz") as tar:
        # Check DS_001.csv
        ds1_member = tar.getmember("DS_001.csv")
        ds1_file = tar.extractfile(ds1_member)
        ds1_content = ds1_file.read().decode('utf-8').strip().splitlines()

        reader = csv.reader(ds1_content)
        ds1_rows = list(reader)

        assert len(ds1_rows) == 3, f"Expected 3 rows in DS_001.csv (1 header, 2 data), found {len(ds1_rows)}"
        assert ds1_rows[0] == ["id", "measurement", "sensor"], f"Incorrect header in DS_001.csv: {ds1_rows[0]}"
        assert ds1_rows[1] == ["101", "42.5", "alpha"], f"Incorrect data row 1 in DS_001.csv: {ds1_rows[1]}"
        assert ds1_rows[2] == ["102", "43.1", "alpha"], f"Incorrect data row 2 in DS_001.csv: {ds1_rows[2]}"

        # Check DS_003.csv
        ds3_member = tar.getmember("DS_003.csv")
        ds3_file = tar.extractfile(ds3_member)
        ds3_content = ds3_file.read().decode('utf-8').strip().splitlines()

        reader = csv.reader(ds3_content)
        ds3_rows = list(reader)

        assert len(ds3_rows) == 3, f"Expected 3 rows in DS_003.csv (1 header, 2 data), found {len(ds3_rows)}"
        assert ds3_rows[0] == ["id", "measurement", "sensor"], f"Incorrect header in DS_003.csv: {ds3_rows[0]}"
        assert ds3_rows[1] == ["301", "99.9", "beta"], f"Incorrect data row 1 in DS_003.csv: {ds3_rows[1]}"
        assert ds3_rows[2] == ["302", "100.1", "beta"], f"Incorrect data row 2 in DS_003.csv: {ds3_rows[2]}"