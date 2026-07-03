# test_final_state.py

import os
import pytest

def test_add_user_mount_script():
    """Verify that the provisioning script exists and is executable."""
    script_path = "/home/user/add_user_mount.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_custom_fstab_contents():
    """Verify that custom_fstab contains the correct entries."""
    fstab_path = "/home/user/custom_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, 'r') as f:
        content = f.read()

    expected_lines = [
        "alice /mnt/alice_data ext4 defaults 0 0",
        "bob /mnt/bob_data xfs defaults 0 0",
        "charlie /mnt/charlie_data ext4 defaults 0 0"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {fstab_path}."

def test_fstab_parser_c_exists():
    """Verify that the C source file exists."""
    c_file_path = "/home/user/fstab_parser.c"
    assert os.path.isfile(c_file_path), f"C source file {c_file_path} does not exist."

def test_fstab_parser_executable():
    """Verify that the compiled C executable exists and is executable."""
    exe_path = "/home/user/fstab_parser"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    # Optional: Check if it's an ELF file
    with open(exe_path, 'rb') as f:
        magic = f.read(4)
        assert magic == b'\x7fELF', f"File {exe_path} is not a valid ELF executable."

def test_fs_summary_log():
    """Verify that the summary log exists and has the correct sorted counts."""
    log_path = "/home/user/fs_summary.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "ext4:2",
        "xfs:1"
    ]

    assert lines == expected_lines, f"Contents of {log_path} do not match the expected output. Got: {lines}"