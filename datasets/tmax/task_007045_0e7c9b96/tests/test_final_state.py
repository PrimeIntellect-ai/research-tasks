# test_final_state.py

import os
import pytest

def test_archiver_c_exists_and_contains_syscalls():
    c_file = '/home/user/archiver.c'
    assert os.path.exists(c_file), f"Source file {c_file} does not exist"

    with open(c_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    assert 'mmap' in content, f"Source file {c_file} does not contain 'mmap'"
    assert 'flock' in content, f"Source file {c_file} does not contain 'flock'"

def test_archive_bin_content():
    bin_file = '/home/user/archive.bin'
    assert os.path.exists(bin_file), f"Output file {bin_file} does not exist"

    expected_data = (
        b'\x05A\x03B\x03C\x09D'
        b'\x02X\x03Y\x02Z'
        b'\xffE\x05E\x0aF'
    )

    with open(bin_file, 'rb') as f:
        actual_data = f.read()

    assert actual_data == expected_data, f"Content of {bin_file} does not match the expected RLE encoding. Expected {len(expected_data)} bytes, got {len(actual_data)} bytes."

def test_original_files_unmodified():
    # Verify log1.dat
    with open('/home/user/log1.dat', 'r') as f:
        assert f.read() == "AAAAABBBCCCDDDDDDDDD", "/home/user/log1.dat was modified"

    # Verify log2.dat
    with open('/home/user/log2.dat', 'r') as f:
        assert f.read() == "XXYYYZZ", "/home/user/log2.dat was modified"

    # Verify log3.dat
    with open('/home/user/log3.dat', 'r') as f:
        assert f.read() == 'E' * 260 + 'F' * 10, "/home/user/log3.dat was modified"

    # Verify backup.conf
    with open('/home/user/backup.conf', 'r') as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]
        assert lines == [
            "/home/user/log1.dat",
            "/home/user/log2.dat",
            "/home/user/log3.dat"
        ], "/home/user/backup.conf was modified"