# test_final_state.py

import os
import pytest

def test_to_archive_txt_content():
    path = "/home/user/to_archive.txt"
    assert os.path.exists(path), f"File {path} is missing."

    expected_content = (
        "[ARCHIVE_ME] Warning: CPU temperature reached 90C!!!!!\n"
        "[ARCHIVE_ME] Critical Error: Memory leak detected in thread 00000000.\n"
        "[ARCHIVE_ME] Shutdown        complete.\n"
    )

    with open(path, "r") as f:
        content = f.read()

    assert content == expected_content, f"Content of {path} does not match the expected filtered new lines."

def test_archive_z_content():
    path = "/home/user/archive.z"
    assert os.path.exists(path), f"File {path} is missing."

    expected_content = (
        "[ARCHIVE_ME] Warning: CPU temperature reached 90C*5!\n"
        "[ARCHIVE_ME] Critical Error: Memory leak detected in thread *80.\n"
        "[ARCHIVE_ME] Shutdown*8 complete.\n"
    )

    with open(path, "r") as f:
        content = f.read()

    assert content == expected_content, f"Content of {path} does not match the expected compressed output."

def test_mmap_compress_c_exists_and_uses_mmap():
    path = "/home/user/mmap_compress.c"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "mmap" in content, f"File {path} does not seem to use mmap."
    assert "munmap" in content, f"File {path} does not seem to use munmap."