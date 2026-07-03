# test_final_state.py

import os
import stat
import pytest

def get_expected_inode(path):
    return os.stat(path).st_ino

def get_expected_hex(path):
    with open(path, "rb") as f:
        data = f.read(8)
    data = data.ljust(8, b'\x00')
    return data.hex()

def test_tracker_c_exists():
    path = "/home/user/tracker.c"
    assert os.path.isfile(path), f"Source file {path} does not exist."

def test_tracker_binary_exists_and_executable():
    path = "/home/user/tracker"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_tracker_err_output():
    path = "/home/user/tracker_err.txt"
    assert os.path.isfile(path), f"Error output file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "SKIP: /home/user/config_tree/link_loop1",
        "SKIP: /home/user/config_tree/link_broken"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected error line '{expected}' not found in {path}"

    assert len(lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} lines in {path}, but found {len(lines)}"

def test_tracker_out_output():
    path = "/home/user/tracker_out.txt"
    assert os.path.isfile(path), f"Standard output file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    file1 = "/home/user/config_tree/file1.bin"
    file2 = "/home/user/config_tree/file2.bin"
    file3 = "/home/user/config_tree/file3.txt"
    link_ok = "/home/user/config_tree/link_ok"

    expected_lines = [
        f"{file1}|{get_expected_inode(file1)}|{get_expected_hex(file1)}",
        f"{file2}|{get_expected_inode(file2)}|{get_expected_hex(file2)}",
        f"{file3}|{get_expected_inode(file3)}|{get_expected_hex(file3)}",
        f"{link_ok}|{get_expected_inode(file1)}|{get_expected_hex(file1)}"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected output line '{expected}' not found in {path}"

    assert len(lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} lines in {path}, but found {len(lines)}"