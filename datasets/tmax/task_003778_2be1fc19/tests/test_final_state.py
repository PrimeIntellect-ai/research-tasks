# test_final_state.py

import os
import time
import tarfile
import pytest

def wait_for_writer():
    pid_file = '/home/user/project/writer.pid'
    if os.path.exists(pid_file):
        with open(pid_file, 'r') as f:
            pid = f.read().strip()
        if pid.isdigit():
            # Wait until the process is no longer running
            while os.path.exists(f"/proc/{pid}"):
                time.sleep(0.1)

def test_symlink_created_correctly():
    symlink_path = '/home/user/project/latest_archive.tar.gz'
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    target = os.readlink(symlink_path)
    assert target.endswith('archive.tar.gz'), f"Symlink points to {target}, expected it to point to archive.tar.gz."

def test_status_file_exists_and_not_empty():
    status_path = '/home/user/project/status.txt'
    assert os.path.isfile(status_path), f"{status_path} does not exist."
    assert os.path.getsize(status_path) > 0, f"{status_path} is empty."

def test_log_rotation_integrity():
    wait_for_writer()

    archive_path = '/home/user/project/archive.tar.gz'
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."

    snapshot_data = ""
    with tarfile.open(archive_path, 'r:gz') as tar:
        snapshot_member = None
        for member in tar.getmembers():
            if member.name.endswith('data_snapshot.log'):
                snapshot_member = member
                break
        assert snapshot_member is not None, "data_snapshot.log not found in archive.tar.gz"

        f = tar.extractfile(snapshot_member)
        assert f is not None, "Failed to extract data_snapshot.log from archive"
        snapshot_data = f.read().decode('utf-8')

    data_log_path = '/home/user/project/data.log'
    assert os.path.isfile(data_log_path), f"{data_log_path} does not exist."

    with open(data_log_path, 'r') as f:
        data_log = f.read()

    combined = snapshot_data + data_log
    lines = [line for line in combined.split('\n') if line]

    assert len(lines) == 3000, f"Expected exactly 3000 log entries, but found {len(lines)}. Data loss or duplication occurred."

    for i, line in enumerate(lines):
        expected_line = f"Log entry {i}"
        assert line == expected_line, f"Sequence broken at line {i+1}. Expected '{expected_line}', got '{line}'."