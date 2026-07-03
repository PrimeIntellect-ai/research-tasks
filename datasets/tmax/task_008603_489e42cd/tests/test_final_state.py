# test_final_state.py

import os
import tarfile
import pytest

def test_loop_log_contents():
    log_path = "/home/user/loop_log.txt"
    assert os.path.exists(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_line = "/home/user/db_backups/cluster2/data/link_back"
    assert len(lines) == 1, f"Expected exactly 1 line in {log_path}, found {len(lines)}."
    assert lines[0] == expected_line, f"Expected line to be '{expected_line}', found '{lines[0]}'."

def test_archive_exists_and_format():
    archive_path = "/home/user/archive.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            pass
    except tarfile.ReadError:
        pytest.fail(f"Archive {archive_path} is not gzip-compressed.")

def test_archive_contents():
    archive_path = "/home/user/archive.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."

    expected_files = {
        "cluster1/node_a/wal_001.log": b"WAL\x01\x00\x11\x22",
        "cluster2/data/wal_003.log": b"WAL\x01\x99\x88\x77",
        "external/wal_004.log": b"WAL\x01\xAA\xBB\xCC"
    }

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()
        file_members = [m for m in members if m.isfile()]
        archived_paths = set(m.name for m in file_members)

        assert archived_paths == set(expected_files.keys()), f"Archive contains incorrect files. Expected {set(expected_files.keys())}, found {archived_paths}."

        for m in file_members:
            f = tar.extractfile(m)
            assert f is not None, f"Could not extract file {m.name} from archive."
            content = f.read()
            expected_content = expected_files[m.name]
            assert content == expected_content, f"Content of {m.name} in archive does not match original."