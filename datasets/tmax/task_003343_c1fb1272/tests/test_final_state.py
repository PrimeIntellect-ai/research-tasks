# test_final_state.py

import os
import csv
import tarfile
import pytest

def test_recovery_log_csv():
    csv_path = "/home/user/recovery_log.csv"
    assert os.path.isfile(csv_path), f"Missing recovery log CSV file: {csv_path}"

    expected_rows = {
        ("bkp-101", "/home/user/backup_vault/dir_A/bkp-101"),
        ("bkp-104", "/home/user/backup_vault/dir_B/sub_C/bkp-104")
    }

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"CSV file {csv_path} is empty.")

        assert headers == ["file_id", "original_path"], \
            f"Incorrect CSV headers. Expected ['file_id', 'original_path'], got {headers}"

        actual_rows = set()
        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Invalid row length in CSV: {row}"
            actual_rows.add(tuple(row))

    assert actual_rows == expected_rows, \
        f"CSV contents do not match expected. Expected {expected_rows}, got {actual_rows}"

def test_alice_recovery_tar():
    tar_path = "/home/user/alice_recovery.tar"
    assert os.path.isfile(tar_path), f"Missing tar archive: {tar_path}"
    assert tarfile.is_tarfile(tar_path), f"File {tar_path} is not a valid tar archive."

    expected_basenames = {"bkp-101", "bkp-104"}

    with tarfile.open(tar_path, "r") as tar:
        members = tar.getmembers()
        # Ensure only files are included, and basenames match exactly
        actual_basenames = {os.path.basename(m.name) for m in members if m.isfile()}

        assert actual_basenames == expected_basenames, \
            f"Tar archive contents do not match expected basenames. Expected {expected_basenames}, got {actual_basenames}"

        # Also ensure no extra directories or unexpected files
        for m in members:
            if m.isfile():
                assert os.path.basename(m.name) in expected_basenames, \
                    f"Unexpected file in tar archive: {m.name}"