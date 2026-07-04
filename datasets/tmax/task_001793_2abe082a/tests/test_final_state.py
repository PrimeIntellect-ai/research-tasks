# test_final_state.py

import os
import pytest

def test_renamed_files_exist():
    """Test that the files have been renamed to UTF-8 with lowercase extensions."""
    dir_path = b"/home/user/legacy_archive"

    expected_files = [
        b"caf\xc3\xa9.txt",
        b"m\xc3\xbcnchen.dat",
        b"r\xc3\xa9sum\xc3\xa9.doc",
        b"normal_file.csv"
    ]

    actual_files = os.listdir(dir_path)

    for filename in expected_files:
        assert filename in actual_files, f"Expected file {filename!r} not found in {dir_path!r}."

def test_old_files_removed():
    """Test that the old ISO-8859-1 files with uppercase extensions are gone."""
    dir_path = b"/home/user/legacy_archive"

    old_files = [
        b"caf\xe9.TXT",
        b"m\xfcnchen.DAT",
        b"r\xe9sum\xe9.DOC",
        b"normal_file.CSV"
    ]

    actual_files = os.listdir(dir_path)

    for filename in old_files:
        assert filename not in actual_files, f"Old file {filename!r} should have been renamed."

def test_log_file_contents():
    """Test that the normalization.log contains the correct mapping lines."""
    log_path = b"/home/user/normalization.log"
    assert os.path.isfile(log_path), "normalization.log does not exist."

    expected_lines = [
        b"/home/user/legacy_archive/caf\xe9.TXT -> /home/user/legacy_archive/caf\xc3\xa9.txt",
        b"/home/user/legacy_archive/m\xfcnchen.DAT -> /home/user/legacy_archive/m\xc3\xbcnchen.dat",
        b"/home/user/legacy_archive/r\xe9sum\xe9.DOC -> /home/user/legacy_archive/r\xc3\xa9sum\xc3\xa9.doc",
        b"/home/user/legacy_archive/normal_file.CSV -> /home/user/legacy_archive/normal_file.csv"
    ]

    with open(log_path, "rb") as f:
        content = f.read()

    for line in expected_lines:
        assert line in content, f"Expected log entry {line!r} not found in normalization.log."