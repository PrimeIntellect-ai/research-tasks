# test_final_state.py

import os
import pytest

UNPACKED_LOGS_DIR = '/home/user/unpacked_logs'
RESULTS_FILE = '/home/user/results.txt'
DEDUP_C = '/home/user/dedup.c'
DEDUP_BIN = '/home/user/dedup'

def test_results_file_contents():
    """Verify that results.txt contains the correct sorted list of filenames."""
    assert os.path.isfile(RESULTS_FILE), f"{RESULTS_FILE} does not exist."
    with open(RESULTS_FILE, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ['f1.log', 'f2.log', 'f3.log', 'f4.log', 'f5.log']
    assert lines == expected, f"Contents of {RESULTS_FILE} do not match expected output. Got: {lines}"

def test_symlinks_deleted():
    """Verify that symlinks have been deleted from the unpacked_logs directory."""
    sym1 = os.path.join(UNPACKED_LOGS_DIR, 'sym1.log')
    sym2 = os.path.join(UNPACKED_LOGS_DIR, 'sym2.log')
    assert not os.path.exists(sym1) and not os.path.islink(sym1), "sym1.log was not deleted."
    assert not os.path.exists(sym2) and not os.path.islink(sym2), "sym2.log was not deleted."

def test_hardlinks_created_correctly():
    """Verify that duplicate files have been hardlinked correctly."""
    f1 = os.path.join(UNPACKED_LOGS_DIR, 'f1.log')
    f2 = os.path.join(UNPACKED_LOGS_DIR, 'f2.log')
    f3 = os.path.join(UNPACKED_LOGS_DIR, 'f3.log')
    f4 = os.path.join(UNPACKED_LOGS_DIR, 'f4.log')
    f5 = os.path.join(UNPACKED_LOGS_DIR, 'f5.log')

    for f in [f1, f2, f3, f4, f5]:
        assert os.path.isfile(f), f"File {f} is missing."

    stat1 = os.stat(f1)
    stat2 = os.stat(f2)
    stat3 = os.stat(f3)
    stat4 = os.stat(f4)
    stat5 = os.stat(f5)

    assert stat1.st_ino == stat2.st_ino, "f1.log and f2.log should be hardlinked (same inode)."
    assert stat3.st_ino == stat5.st_ino, "f3.log and f5.log should be hardlinked (same inode)."
    assert stat4.st_ino != stat1.st_ino and stat4.st_ino != stat3.st_ino, "f4.log should not be hardlinked to the others."

    # Total unique inodes among the 5 files should be exactly 3
    inodes = {stat1.st_ino, stat2.st_ino, stat3.st_ino, stat4.st_ino, stat5.st_ino}
    assert len(inodes) == 3, f"Expected exactly 3 unique inodes among the log files, found {len(inodes)}."

def test_file_contents_preserved():
    """Verify that the contents of the files are correct and were not altered."""
    f1 = os.path.join(UNPACKED_LOGS_DIR, 'f1.log')
    f3 = os.path.join(UNPACKED_LOGS_DIR, 'f3.log')
    f4 = os.path.join(UNPACKED_LOGS_DIR, 'f4.log')

    with open(f1, 'r') as f:
        assert f.read().strip() == "LOG_DATA_A_123", "Content of f1.log/f2.log is incorrect."
    with open(f3, 'r') as f:
        assert f.read().strip() == "LOG_DATA_B_456", "Content of f3.log/f5.log is incorrect."
    with open(f4, 'r') as f:
        assert f.read().strip() == "LOG_DATA_C_789", "Content of f4.log is incorrect."

def test_dedup_program_exists():
    """Verify that the dedup C source and executable exist."""
    assert os.path.isfile(DEDUP_C), f"{DEDUP_C} source file is missing."
    assert os.path.isfile(DEDUP_BIN), f"{DEDUP_BIN} executable is missing."
    assert os.access(DEDUP_BIN, os.X_OK), f"{DEDUP_BIN} is not executable."

def test_no_extra_files():
    """Verify that no corrupted files or extra unexpected files were extracted."""
    expected_files = {'f1.log', 'f2.log', 'f3.log', 'f4.log', 'f5.log'}
    actual_files = set(os.listdir(UNPACKED_LOGS_DIR))
    assert actual_files == expected_files, f"Unexpected files found in {UNPACKED_LOGS_DIR}: {actual_files - expected_files}"