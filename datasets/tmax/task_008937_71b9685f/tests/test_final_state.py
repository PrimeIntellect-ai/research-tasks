# test_final_state.py

import os
import tarfile
import pytest

DUMPS_DIR = "/home/user/dumps"
SCANNER_C = "/home/user/scanner.c"
OLD_FILES_TXT = "/home/user/old_files.txt"
ARCHIVE_PATH = "/home/user/old_dumps.tar.gz"

EXPECTED_OLD_FILES = {"dump_01.bin", "dump_03.bin", "dump_05.bin"}
EXPECTED_NEW_FILES = {"dump_02.bin", "dump_04.bin"}

def test_scanner_c_exists_and_uses_mmap():
    assert os.path.isfile(SCANNER_C), f"Fail: {SCANNER_C} does not exist"
    with open(SCANNER_C, "r", encoding="utf-8") as f:
        content = f.read()
    assert "mmap" in content, f"Fail: {SCANNER_C} does not seem to use mmap (missing 'mmap' keyword)"
    assert "<sys/mman.h>" in content, f"Fail: {SCANNER_C} does not include <sys/mman.h>"

def test_old_files_txt_content():
    assert os.path.isfile(OLD_FILES_TXT), f"Fail: {OLD_FILES_TXT} does not exist"
    with open(OLD_FILES_TXT, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_paths = {os.path.join(DUMPS_DIR, fname) for fname in EXPECTED_OLD_FILES}
    actual_paths = set(lines)

    assert len(lines) == len(expected_paths), f"Fail: {OLD_FILES_TXT} should contain exactly {len(expected_paths)} lines, found {len(lines)}"
    assert actual_paths == expected_paths, f"Fail: {OLD_FILES_TXT} does not contain the correct absolute paths. Expected {expected_paths}, got {actual_paths}"

def test_remaining_files_in_dumps_dir():
    assert os.path.isdir(DUMPS_DIR), f"Fail: {DUMPS_DIR} does not exist"
    actual_files = set(os.listdir(DUMPS_DIR))

    assert actual_files == EXPECTED_NEW_FILES, f"Fail: {DUMPS_DIR} should contain exactly {EXPECTED_NEW_FILES}, but contains {actual_files}"

def test_archive_exists_and_contains_old_files():
    assert os.path.isfile(ARCHIVE_PATH), f"Fail: {ARCHIVE_PATH} does not exist"
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"Fail: {ARCHIVE_PATH} is not a valid tar archive"

    try:
        with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
            members = tar.getnames()
    except Exception as e:
        pytest.fail(f"Fail: Could not read {ARCHIVE_PATH} as a gzipped tarball. Error: {e}")

    # Extract just the basenames to handle both absolute and relative path archiving
    archived_basenames = {os.path.basename(m) for m in members if m.endswith('.bin')}

    assert archived_basenames == EXPECTED_OLD_FILES, f"Fail: Archive contains incorrect files. Expected {EXPECTED_OLD_FILES}, got {archived_basenames}"