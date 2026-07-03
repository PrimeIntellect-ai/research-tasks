# test_final_state.py

import os
import tarfile
import hashlib
import gzip
from pathlib import Path
import pytest

def get_expected_filenames():
    expected_names = []
    base_dir = Path('/home/user/logs_staging')
    for p in base_dir.rglob('*.log.gz'):
        with gzip.open(p, 'rt') as f:
            first_line = f.readline()
            # Extract date from format: LogEntry: [YYYY-MM-DD] - <message>
            date = first_line.split('[')[1].split(']')[0]
        with open(p, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        expected_names.append(f"{date}_{md5}.log.gz")
    expected_names.sort()
    return expected_names

def test_archive_report():
    report_path = '/home/user/archive_report.txt'
    assert os.path.isfile(report_path), f"Report file missing: {report_path}"

    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_names = get_expected_filenames()
    assert lines == expected_names, "The contents of archive_report.txt do not match the expected sorted list of filenames."

def test_master_archive():
    tar_path = '/home/user/master_archive.tar'
    assert os.path.isfile(tar_path), f"Tar archive missing: {tar_path}"

    assert tarfile.is_tarfile(tar_path), f"File {tar_path} is not a valid tar archive."

    with tarfile.open(tar_path, 'r') as tar:
        members = tar.getnames()

    expected_names = get_expected_filenames()

    assert sorted(members) == expected_names, "The files inside the tar archive do not match the expected renamed files."

def test_master_archive_is_uncompressed():
    tar_path = '/home/user/master_archive.tar'
    assert os.path.isfile(tar_path), f"Tar archive missing: {tar_path}"

    # Ensure it's not compressed (e.g. gzip or bz2)
    with open(tar_path, 'rb') as f:
        header = f.read(2)
        # Gzip magic number
        assert header != b'\x1f\x8b', "The tar archive should be uncompressed, but it appears to be gzipped."
        # Bzip2 magic number
        assert header != b'BZ', "The tar archive should be uncompressed, but it appears to be bzip2 compressed."