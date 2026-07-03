# test_final_state.py

import os
import tarfile
import pytest

V1_DIR = '/home/user/snapshots/v1'
V2_DIR = '/home/user/snapshots/v2'
RAW_DIR = '/home/user/raw_data'
TAR_PATH = '/home/user/patch_v1_to_v2.tar.gz'
REPORT_PATH = '/home/user/report.txt'

def test_v2_directory_exists():
    assert os.path.isdir(V2_DIR), f"The destination directory {V2_DIR} was not created."

def test_v2_matches_raw_data():
    raw_files = set(os.listdir(RAW_DIR))
    v2_files = set(os.listdir(V2_DIR))

    assert raw_files == v2_files, f"Files in {V2_DIR} do not match {RAW_DIR}. Expected {raw_files}, got {v2_files}"

    for filename in raw_files:
        raw_path = os.path.join(RAW_DIR, filename)
        v2_path = os.path.join(V2_DIR, filename)

        with open(raw_path, 'rb') as f1, open(v2_path, 'rb') as f2:
            assert f1.read() == f2.read(), f"Content of {v2_path} does not match {raw_path}"

def test_hardlinks_for_unmodified_files():
    # unchanged1.txt and unchanged2.txt should be hardlinked from v1 to v2
    for filename in ['unchanged1.txt', 'unchanged2.txt']:
        v1_path = os.path.join(V1_DIR, filename)
        v2_path = os.path.join(V2_DIR, filename)

        assert os.path.exists(v1_path), f"Expected file {v1_path} is missing."
        assert os.path.exists(v2_path), f"Expected file {v2_path} is missing."

        stat_v1 = os.stat(v1_path)
        stat_v2 = os.stat(v2_path)

        assert stat_v1.st_ino == stat_v2.st_ino, f"File {filename} is not hardlinked between v1 and v2."

def test_no_hardlinks_for_modified_files():
    # modified1.txt should NOT be hardlinked
    filename = 'modified1.txt'
    v1_path = os.path.join(V1_DIR, filename)
    v2_path = os.path.join(V2_DIR, filename)

    assert os.path.exists(v1_path), f"Expected file {v1_path} is missing."
    assert os.path.exists(v2_path), f"Expected file {v2_path} is missing."

    stat_v1 = os.stat(v1_path)
    stat_v2 = os.stat(v2_path)

    assert stat_v1.st_ino != stat_v2.st_ino, f"File {filename} is incorrectly hardlinked between v1 and v2."

def test_patch_archive_contents():
    assert os.path.isfile(TAR_PATH), f"Patch archive {TAR_PATH} is missing."

    with tarfile.open(TAR_PATH, 'r:gz') as tar:
        names = tar.getnames()
        # Remove leading './' if present
        normalized_names = {n.lstrip('./') for n in names}

        # Should only contain modified and new files
        expected = {'modified1.txt', 'new1.txt', 'new2.txt'}
        assert expected == normalized_names, f"Tarball contents incorrect. Expected {expected}, got {normalized_names}"

def test_report_contents():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} is missing."

    with open(REPORT_PATH, 'r') as f:
        report = f.read().strip()

    assert "New files: 2" in report, "Report does not correctly state 'New files: 2'"
    assert "Modified files: 1" in report, "Report does not correctly state 'Modified files: 1'"
    assert "Unmodified files: 2" in report, "Report does not correctly state 'Unmodified files: 2'"