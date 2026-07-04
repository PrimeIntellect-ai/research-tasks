# test_final_state.py

import os
import pytest

LOGS_DIR = "/home/user/logs"
RESOLVER_GO = "/home/user/resolver.go"
RECOVERY_TXT = os.path.join(LOGS_DIR, "full_recovery.txt")

def test_resolver_go_exists_and_uses_flock():
    assert os.path.isfile(RESOLVER_GO), f"File {RESOLVER_GO} does not exist."
    with open(RESOLVER_GO, "r") as f:
        content = f.read()
    assert "syscall.Flock" in content, f"syscall.Flock is not used in {RESOLVER_GO}."

def test_full_recovery_file_exists_and_has_50_lines():
    assert os.path.isfile(RECOVERY_TXT), f"Output file {RECOVERY_TXT} does not exist."
    with open(RECOVERY_TXT, "r") as f:
        lines = f.readlines()

    # Filter out empty lines if any, though the task expects exactly 50
    non_empty_lines = [line for line in lines if line.strip()]
    assert len(non_empty_lines) == 50, f"Expected 50 lines in {RECOVERY_TXT}, found {len(non_empty_lines)}."

def test_full_recovery_content():
    # Verify that all expected log entries are present in the recovery file
    with open(RECOVERY_TXT, "r") as f:
        content = f.read()

    for i in range(1, 51):
        num_str = f"{i:03d}"
        expected_entry = f"CRITICAL_LOG_ENTRY_{num_str}: System state stable at timestamp {num_str}000"
        assert expected_entry in content, f"Missing expected log entry in {RECOVERY_TXT}: {expected_entry}"

def test_part_files_are_gone():
    part_files = [f for f in os.listdir(LOGS_DIR) if f.endswith(".part")]
    assert len(part_files) == 0, f"Found unexpected .part files in {LOGS_DIR}: {part_files}"

def test_done_files_exist_and_correct_count():
    done_files = [f for f in os.listdir(LOGS_DIR) if f.endswith(".done")]
    assert len(done_files) == 50, f"Expected 50 .done files in {LOGS_DIR}, found {len(done_files)}."

    # Ensure specific files exist
    for i in range(1, 51):
        num_str = f"{i:03d}"
        expected_file = f"syslog_{num_str}.done"
        assert expected_file in done_files, f"Missing expected file {expected_file} in {LOGS_DIR}."

def test_symlink_loop_still_exists():
    symlink_path = os.path.join(LOGS_DIR, "loop_link")
    assert os.path.islink(symlink_path), f"Symlink {symlink_path} does not exist or is not a symlink."
    assert os.readlink(symlink_path) == ".", f"Symlink {symlink_path} does not point to '.'."