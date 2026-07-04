# test_final_state.py

import os
import subprocess
import pytest

TARGET_DIR = "/app/bloated_dir"
THRESHOLD_SIZE = 1500000

def test_directory_size():
    """
    Verify that the total disk usage of the target directory is strictly below the threshold.
    This effectively checks if the duplicate 1MB files were successfully hard-linked.
    """
    assert os.path.isdir(TARGET_DIR), f"Target directory missing: {TARGET_DIR}"

    try:
        output = subprocess.check_output(['du', '-sb', TARGET_DIR], text=True)
        size = int(output.split()[0])
    except Exception as e:
        pytest.fail(f"Failed to calculate directory size: {e}")

    assert size < THRESHOLD_SIZE, f"Directory size {size} is not below the threshold {THRESHOLD_SIZE}. Deduplication may have failed."

def test_malicious_symlinks_remediated():
    """
    Verify that symlinks pointing outside the target directory were removed and replaced
    with a regular text file containing 'INVALID_LINK_REMOVED'.
    """
    malicious_links = [
        "/app/bloated_dir/configs/passwd_link",
        "/app/bloated_dir/cache/log_link",
        "/app/bloated_dir/cache/shadow_link"
    ]

    for path in malicious_links:
        assert os.path.exists(path), f"Expected file at {path} is missing."
        assert not os.path.islink(path), f"File at {path} is still a symlink, but should have been replaced."
        assert os.path.isfile(path), f"File at {path} is not a regular file."

        with open(path, "r") as f:
            content = f.read().strip()

        assert content == "INVALID_LINK_REMOVED", f"File at {path} contains incorrect content: '{content}' instead of 'INVALID_LINK_REMOVED'."

def test_safe_symlink_preserved():
    """
    Verify that a symlink pointing inside the target directory was NOT removed.
    """
    safe_link = "/app/bloated_dir/logs/safe_link"
    expected_target = "/app/bloated_dir/configs/c1.cfg"

    assert os.path.islink(safe_link), f"Safe symlink at {safe_link} was incorrectly removed or altered."
    target = os.readlink(safe_link)
    assert target == expected_target, f"Safe symlink points to {target} instead of {expected_target}."

def test_hard_links_created():
    """
    Verify that the duplicate log files actually share the same inode (hard-linked).
    """
    log1 = "/app/bloated_dir/logs/log_1.dat"
    log2 = "/app/bloated_dir/logs/log_2.dat"

    assert os.path.exists(log1), f"Log file missing: {log1}"
    assert os.path.exists(log2), f"Log file missing: {log2}"

    stat1 = os.stat(log1)
    stat2 = os.stat(log2)

    assert stat1.st_ino == stat2.st_ino, "Duplicate log files do not share the same inode. Hard-linking failed."
    assert stat1.st_nlink > 1, f"Log file at {log1} does not have multiple hard links (nlink={stat1.st_nlink})."