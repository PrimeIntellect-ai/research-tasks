# test_final_state.py

import os
import pytest

def test_rust_files_exist():
    """Check if the Rust source file and compiled executable exist."""
    source_file = "/home/user/decode_rle.rs"
    executable_file = "/home/user/decode_rle"

    assert os.path.isfile(source_file), f"Rust source file {source_file} is missing."
    assert os.path.isfile(executable_file), f"Compiled executable {executable_file} is missing."
    assert os.access(executable_file, os.X_OK), f"File {executable_file} is not executable."

def test_oom_events_content():
    """Check if the oom_events.log contains the correct sorted output."""
    log_file = "/home/user/oom_events.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    expected_lines = [
        "CRITICAL_OOM: postgresql process terminated\n",
        "CRITICAL_OOM: redis cache memory limit exceeded\n",
        "CRITICAL_OOM: worker thread out of memory\n"
    ]

    with open(log_file, "r") as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, (
        f"Content of {log_file} does not match expected output.\n"
        f"Expected:\n{''.join(expected_lines)}\n"
        f"Actual:\n{''.join(actual_lines)}"
    )

def test_symlink():
    """Check if the latest_incident symlink is correctly created."""
    symlink_path = "/home/user/latest_incident"
    target_path = "/home/user/oom_events.log"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    actual_target = os.readlink(symlink_path)
    # The symlink could be absolute or relative, resolve it to check
    if not os.path.isabs(actual_target):
        actual_target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), actual_target))

    assert actual_target == target_path, (
        f"Symlink {symlink_path} points to {actual_target} instead of {target_path}."
    )