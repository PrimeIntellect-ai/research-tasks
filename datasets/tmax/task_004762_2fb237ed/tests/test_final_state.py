# test_final_state.py

import os
import tarfile

def test_symlink_deleted():
    loop_symlink = "/home/user/data/docs/logs/archive"
    assert not os.path.lexists(loop_symlink), f"The looping symlink {loop_symlink} was not deleted."

def test_archive_exists_and_dereferenced():
    archive_path = "/home/user/backup.tar.gz"
    assert os.path.isfile(archive_path), f"The archive {archive_path} does not exist."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            # Find metrics.json in the archive
            metrics_member = None
            for member in tar.getmembers():
                if member.name.endswith("data/metrics.json"):
                    metrics_member = member
                    break

            assert metrics_member is not None, "data/metrics.json was not found in the archive."
            assert metrics_member.isreg(), "data/metrics.json in the archive is not a regular file (symlinks were not dereferenced)."
    except tarfile.ReadError:
        assert False, f"{archive_path} is not a valid gzip compressed tarball."

def test_csv_correct():
    csv_path = "/home/user/metrics.csv"
    assert os.path.isfile(csv_path), f"The CSV file {csv_path} does not exist."

    expected_csv = [
        "id,value,status",
        "101,42.5,active",
        "102,89.1,pending",
        "103,12.0,error"
    ]

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_csv, f"The contents of {csv_path} do not match the expected CSV format and data."