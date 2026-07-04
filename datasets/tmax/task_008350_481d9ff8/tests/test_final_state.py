# test_final_state.py

import os
import re
import pytest

def test_extracted_files_exist():
    log_path = "/home/user/restored/qemu_vnc.log"
    disk_path = "/home/user/restored/disk.img"

    assert os.path.exists(log_path), f"Extracted log file is missing: {log_path}"
    assert os.path.isfile(log_path), f"Path is not a file: {log_path}"

    assert os.path.exists(disk_path), f"Extracted disk image is missing: {disk_path}"
    assert os.path.isfile(disk_path), f"Path is not a file: {disk_path}"

def test_vnc_ports_extracted():
    ports_file = "/home/user/vnc_ports.txt"
    assert os.path.exists(ports_file), f"Ports file is missing: {ports_file}"

    with open(ports_file, "r") as f:
        content = f.read().strip()

    ports = [line.strip() for line in content.splitlines() if line.strip()]
    expected_ports = ["5901", "5902", "5905"]

    assert ports == expected_ports, f"Expected ports {expected_ports}, but got {ports}"

def test_rust_program_and_status_output():
    rs_file = "/home/user/test_connectivity.rs"
    bin_file = "/home/user/test_connectivity"
    status_file = "/home/user/restored_vnc_status.txt"

    assert os.path.exists(rs_file), f"Rust source file missing: {rs_file}"
    assert os.path.exists(bin_file), f"Compiled Rust binary missing: {bin_file}"
    assert os.path.exists(status_file), f"Status output file missing: {status_file}"

    with open(status_file, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    expected_lines = [
        "PORT 5901 IS DOWN",
        "PORT 5902 IS UP",
        "PORT 5905 IS DOWN"
    ]

    # Check that all expected lines are present (order independent)
    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {status_file}"

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(lines)} in {status_file}"

def test_fstab_mock_output():
    fstab_file = "/home/user/fstab_test"
    assert os.path.exists(fstab_file), f"Fstab test file missing: {fstab_file}"

    with open(fstab_file, "r") as f:
        content = f.read().strip()

    lines = [line for line in content.splitlines() if line.strip()]
    assert len(lines) == 1, f"Expected exactly one line in {fstab_file}, but got {len(lines)}"

    tokens = lines[0].split()
    expected_tokens = [
        "/home/user/restored/disk.img",
        "/mnt/restored",
        "ext4",
        "loop,ro",
        "0",
        "0"
    ]

    assert tokens == expected_tokens, f"Expected fstab tokens {expected_tokens}, but got {tokens}"