# test_final_state.py

import os
import pytest

def test_safe_configs_hard_links():
    incoming_dir = "/home/user/incoming_configs"
    safe_dir = "/home/user/safe_configs"

    expected_safe = ["app1_update.tar", "app2_update.tar"]

    for filename in expected_safe:
        incoming_path = os.path.join(incoming_dir, filename)
        safe_path = os.path.join(safe_dir, filename)

        assert os.path.exists(safe_path), f"Safe config missing: {safe_path}"
        assert not os.path.islink(safe_path), f"Expected hard link, but found symlink for {safe_path}"

        incoming_stat = os.stat(incoming_path)
        safe_stat = os.stat(safe_path)

        assert incoming_stat.st_ino == safe_stat.st_ino, f"Inode mismatch for {filename}: not a hard link"

def test_quarantine_configs_symlinks():
    incoming_dir = "/home/user/incoming_configs"
    quarantine_dir = "/home/user/quarantine_configs"

    expected_malicious = ["evil_relative.tar", "evil_absolute.tar"]

    for filename in expected_malicious:
        incoming_path = os.path.join(incoming_dir, filename)
        quarantine_path = os.path.join(quarantine_dir, filename)

        assert os.path.exists(quarantine_path) or os.path.islink(quarantine_path), f"Quarantine config missing: {quarantine_path}"
        assert os.path.islink(quarantine_path), f"Expected symlink for {quarantine_path}"

        target = os.readlink(quarantine_path)
        # Handle both absolute and relative symlinks correctly by resolving them
        assert os.path.abspath(os.path.join(quarantine_dir, target)) == os.path.abspath(incoming_path), f"Symlink target mismatch for {filename}"

def test_corrupted_log():
    log_path = "/home/user/corrupted.log"
    assert os.path.isfile(log_path), f"Corrupted log file missing: {log_path}"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_corrupted = {"broken1.tar", "broken2.tar"}
    assert set(lines) == expected_corrupted, f"Corrupted log contents mismatch. Expected {expected_corrupted}, got {set(lines)}"
    assert len(lines) == 2, f"Corrupted log should contain exactly 2 lines, got {len(lines)}"

def test_compiled_binary_exists():
    binary_path = "/home/user/config_filter"
    assert os.path.isfile(binary_path), f"Compiled binary missing: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Compiled binary is not executable: {binary_path}"

def test_no_extra_files_in_directories():
    safe_dir = "/home/user/safe_configs"
    quarantine_dir = "/home/user/quarantine_configs"

    safe_files = set(os.listdir(safe_dir))
    quarantine_files = set(os.listdir(quarantine_dir))

    expected_safe = {"app1_update.tar", "app2_update.tar"}
    expected_quarantine = {"evil_relative.tar", "evil_absolute.tar"}

    assert safe_files == expected_safe, f"Unexpected files in safe_configs: {safe_files}"
    assert quarantine_files == expected_quarantine, f"Unexpected files in quarantine_configs: {quarantine_files}"