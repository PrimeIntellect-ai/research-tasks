# test_final_state.py

import os
import pytest

def test_processed_directories_and_files():
    # Check logA.tsv
    logA_path = "/home/user/backups/processed/2024-05-01/logA.tsv"
    assert os.path.isfile(logA_path), f"File {logA_path} does not exist"
    with open(logA_path, "r") as f:
        content_A = f.read().strip()
    expected_A = "101\t2024-05-01\tlogin\n102\t2024-05-01\tlogout"
    assert content_A == expected_A, f"Content mismatch in {logA_path}"

    # Check logB.tsv
    logB_path = "/home/user/backups/processed/2024-05-02/logB.tsv"
    assert os.path.isfile(logB_path), f"File {logB_path} does not exist"
    with open(logB_path, "r") as f:
        content_B = f.read().strip()
    expected_B = "103\t2024-05-02\tupload\n104\t2024-05-02\tdownload"
    assert content_B == expected_B, f"Content mismatch in {logB_path}"

    # Check logD.tsv
    logD_path = "/home/user/backups/processed/2024-04-30/logD.tsv"
    assert os.path.isfile(logD_path), f"File {logD_path} does not exist"
    with open(logD_path, "r") as f:
        content_D = f.read().strip()
    expected_D = "99\t2024-04-30\tregister"
    assert content_D == expected_D, f"Content mismatch in {logD_path}"

def test_hard_links():
    logA_path = "/home/user/backups/processed/2024-05-01/logA.tsv"
    logC_path = "/home/user/backups/processed/2024-05-01/logC.tsv"

    assert os.path.isfile(logA_path), f"File {logA_path} does not exist"
    assert os.path.isfile(logC_path), f"File {logC_path} does not exist"

    inode_A = os.stat(logA_path).st_ino
    inode_C = os.stat(logC_path).st_ino

    assert inode_A == inode_C, f"{logA_path} and {logC_path} are not hardlinked (different inodes)"

def test_symlink_latest():
    symlink_path = "/home/user/backups/latest"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link"

    target = os.readlink(symlink_path)
    # The target could be absolute or relative. Let's resolve it.
    resolved_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))

    expected_target = "/home/user/backups/processed/2024-05-02"
    assert resolved_target == expected_target, f"Symlink points to {resolved_target} instead of {expected_target}"