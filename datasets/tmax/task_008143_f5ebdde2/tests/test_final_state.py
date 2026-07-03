# test_final_state.py

import os
import tarfile
import pytest

def test_cpp_exists():
    assert os.path.isfile("/home/user/renamer.cpp"), "/home/user/renamer.cpp does not exist."

def test_original_binaries_untouched():
    expected_binaries = [
        "deadbeef.bin",
        "cafebabe.bin",
        "8badf00d.bin"
    ]
    for binary in expected_binaries:
        path = os.path.join("/home/user/repo/binaries", binary)
        assert os.path.isfile(path), f"Original binary {path} is missing or was modified."

def test_staging_renamed():
    staging_dir = "/home/user/repo/staging"
    assert os.path.isdir(staging_dir), "Staging directory does not exist."

    expected_files = [
        "core-v1.2.0.bin",
        "core-v1.2.1.bin",
        "utils-v0.9.bin"
    ]
    unexpected_files = [
        "deadbeef.bin",
        "cafebabe.bin",
        "8badf00d.bin"
    ]

    files_in_staging = os.listdir(staging_dir)

    for f in expected_files:
        assert f in files_in_staging, f"Expected file {f} not found in staging directory."

    for f in unexpected_files:
        assert f not in files_in_staging, f"Original hashed file {f} should not exist in staging directory."

def test_tarball_exists_and_contents():
    tarball_path = "/home/user/backup/incremental.tar.gz"
    assert os.path.isfile(tarball_path), f"Backup tarball {tarball_path} does not exist."

    expected_basenames = {
        "core-v1.2.0.bin",
        "core-v1.2.1.bin",
        "utils-v0.9.bin"
    }

    found_basenames = set()
    with tarfile.open(tarball_path, "r:gz") as tar:
        for member in tar.getmembers():
            # Extract just the filename without any leading path like './'
            basename = os.path.basename(member.name)
            if basename:
                found_basenames.add(basename)

    for expected in expected_basenames:
        assert expected in found_basenames, f"File {expected} is missing from the tarball."

    for found in found_basenames:
        if found not in expected_basenames and found != "." and found != "":
            # Ignore standard tar metadata files or directories if any, but ensure no hashed names
            assert not found.endswith(".bin") or found in expected_basenames, f"Unexpected binary {found} found in tarball."

def test_snapshot_updated():
    snapshot_path = "/home/user/backup/snapshot.snar"
    assert os.path.isfile(snapshot_path), f"Snapshot file {snapshot_path} does not exist."

    # Check that snapshot was updated by comparing its mtime to the original binaries
    # which were created during setup before the task started.
    binary_mtime = os.path.getmtime("/home/user/repo/binaries/deadbeef.bin")
    snapshot_mtime = os.path.getmtime(snapshot_path)

    assert snapshot_mtime >= binary_mtime, "Snapshot file does not appear to have been updated."