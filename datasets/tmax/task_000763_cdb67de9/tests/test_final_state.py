# test_final_state.py

import os
import subprocess
import tarfile
import pytest

def test_backup_filter_executable():
    """Check if the backup_filter program exists and is executable."""
    executable_path = "/home/user/backup_filter"
    assert os.path.isfile(executable_path), f"Missing executable at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_backup_filter_evil_corpus():
    """Check if the backup_filter correctly rejects evil files."""
    executable_path = "/home/user/backup_filter"
    evil_dir = "/app/verifier_corpus/evil"

    assert os.path.isdir(evil_dir), f"Missing evil corpus directory at {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "Evil corpus directory is empty"

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([executable_path, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed: {', '.join(bypassed_files)}")

def test_backup_filter_clean_corpus():
    """Check if the backup_filter correctly accepts clean files."""
    executable_path = "/home/user/backup_filter"
    clean_dir = "/app/verifier_corpus/clean"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory at {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "Clean corpus directory is empty"

    rejected_files = []
    for filepath in clean_files:
        result = subprocess.run([executable_path, filepath], capture_output=True)
        if result.returncode != 0:
            rejected_files.append(os.path.basename(filepath))

    if rejected_files:
        pytest.fail(f"{len(rejected_files)} of {len(clean_files)} clean files rejected: {', '.join(rejected_files)}")

def test_backup_tarball_exists_and_valid():
    """Check if the backup tarball exists and is a valid gzip-compressed tarball."""
    tarball_path = "/home/user/backup.tar.gz"
    assert os.path.isfile(tarball_path), f"Missing backup tarball at {tarball_path}"
    assert tarfile.is_tarfile(tarball_path), f"File at {tarball_path} is not a valid tarball"

    # Check if it is gzipped
    with open(tarball_path, 'rb') as f:
        magic = f.read(2)
        assert magic == b'\x1f\x8b', f"File at {tarball_path} is not gzip compressed"

def test_backup_tarball_contents():
    """Check if the backup tarball contains the correctly renamed .safe files from the clean subset of raw_data."""
    tarball_path = "/home/user/backup.tar.gz"
    raw_data_dir = "/home/user/raw_data"

    assert os.path.isfile(tarball_path), f"Missing backup tarball at {tarball_path}"
    assert os.path.isdir(raw_data_dir), f"Missing raw data directory at {raw_data_dir}"

    # Determine the expected clean files from raw_data
    expected_safe_files = set()
    for filename in os.listdir(raw_data_dir):
        filepath = os.path.join(raw_data_dir, filename)
        if not os.path.isfile(filepath):
            continue

        with open(filepath, 'rb') as f:
            content = f.read()

        is_evil = False
        if content.startswith(b'EVIL'):
            is_evil = True
        elif b'DO_NOT_BACKUP' in content:
            is_evil = True

        if not is_evil:
            expected_safe_files.add(filename + ".safe")

    # Read the tarball contents
    with tarfile.open(tarball_path, "r:gz") as tar:
        tar_members = tar.getnames()

    # Extract just the basenames from the tarball to handle different archiving paths (e.g., safe_data/file.txt.safe vs file.txt.safe)
    tar_basenames = {os.path.basename(m) for m in tar_members if not m.endswith('/')}

    missing_files = expected_safe_files - tar_basenames
    extra_files = tar_basenames - expected_safe_files

    error_msgs = []
    if missing_files:
        error_msgs.append(f"Missing safe files in tarball: {', '.join(missing_files)}")
    if extra_files:
        error_msgs.append(f"Unexpected files in tarball: {', '.join(extra_files)}")

    if error_msgs:
        pytest.fail("; ".join(error_msgs))