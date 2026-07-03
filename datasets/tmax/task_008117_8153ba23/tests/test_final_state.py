# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/storage_pool"
LOGS_DIR = os.path.join(BASE_DIR, "logs")
CRITICAL_DIR = os.path.join(BASE_DIR, "critical")
INTENDED_DIR = os.path.join(BASE_DIR, "intended")

def test_phase1_critical_files_encoding():
    mal1 = os.path.join(CRITICAL_DIR, "malicious_1.conf")
    mal2 = os.path.join(CRITICAL_DIR, "malicious_2.conf")
    fail_hack = os.path.join(CRITICAL_DIR, "failed_hack.conf")
    sys_conf = os.path.join(CRITICAL_DIR, "system.conf")

    assert os.path.isfile(mal1), f"File missing: {mal1}"
    assert os.path.isfile(mal2), f"File missing: {mal2}"
    assert os.path.isfile(fail_hack), f"File missing: {fail_hack}"

    # Check that malicious_1.conf and malicious_2.conf are now UTF-8
    with open(mal1, "rb") as f:
        content1 = f.read()
        try:
            decoded1 = content1.decode("utf-8")
            assert decoded1 == "malicious content 1", "malicious_1.conf content changed or incorrect"
        except UnicodeDecodeError:
            pytest.fail("malicious_1.conf is not properly UTF-8 encoded")

    with open(mal2, "rb") as f:
        content2 = f.read()
        try:
            decoded2 = content2.decode("utf-8")
            assert decoded2 == "malicious content 2", "malicious_2.conf content changed or incorrect"
        except UnicodeDecodeError:
            pytest.fail("malicious_2.conf is not properly UTF-8 encoded")

    # Check that failed_hack.conf remains unchanged (UTF-8)
    with open(fail_hack, "rb") as f:
        content3 = f.read()
        try:
            decoded3 = content3.decode("utf-8")
            assert decoded3 == "normal system config", "failed_hack.conf content changed"
        except UnicodeDecodeError:
            pytest.fail("failed_hack.conf should remain UTF-8 encoded")

def test_phase2_and_3_intended_files():
    expected_files = [
        "file_a.bak",
        "file_b.bak",
        "file_c.bak",
        "data_report_1.bak",
        "data_report_2.bak"
    ]

    # Check that files were renamed correctly
    for filename in expected_files:
        filepath = os.path.join(INTENDED_DIR, filename)
        assert os.path.isfile(filepath), f"Expected file missing or not renamed properly: {filepath}"

    # Check that old files do not exist
    old_files = [
        "file_a.dat",
        "file b.dat",
        "file_c.dat",
        "data report 1.dat",
        "data_report_2.dat"
    ]
    for filename in old_files:
        filepath = os.path.join(INTENDED_DIR, filename)
        assert not os.path.exists(filepath), f"Old file still exists: {filepath}"

    # Check deduplication (inodes)
    file_a = os.path.join(INTENDED_DIR, "file_a.bak")
    file_b = os.path.join(INTENDED_DIR, "file_b.bak")
    file_c = os.path.join(INTENDED_DIR, "file_c.bak")

    inode_a = os.stat(file_a).st_ino
    inode_b = os.stat(file_b).st_ino
    inode_c = os.stat(file_c).st_ino

    assert inode_a == inode_b == inode_c, "file_a.bak, file_b.bak, and file_c.bak do not share the same inode (not hard linked)"

    data_1 = os.path.join(INTENDED_DIR, "data_report_1.bak")
    data_2 = os.path.join(INTENDED_DIR, "data_report_2.bak")

    inode_d1 = os.stat(data_1).st_ino
    inode_d2 = os.stat(data_2).st_ino

    assert inode_d1 == inode_d2, "data_report_1.bak and data_report_2.bak do not share the same inode (not hard linked)"

def test_log_file_untouched():
    log_file = os.path.join(LOGS_DIR, "extract.log")
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"