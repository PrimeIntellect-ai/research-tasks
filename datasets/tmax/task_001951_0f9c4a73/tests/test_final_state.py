# test_final_state.py
import os
import pytest

def test_hasher_c_exists():
    assert os.path.isfile('/home/user/hasher.c'), "/home/user/hasher.c does not exist."

def test_hasher_executable_exists():
    assert os.path.isfile('/home/user/hasher'), "/home/user/hasher does not exist."
    assert os.access('/home/user/hasher', os.X_OK), "/home/user/hasher is not executable."

def test_manifest_content():
    manifest_path = '/home/user/manifest.txt'
    assert os.path.isfile(manifest_path), f"{manifest_path} does not exist."

    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected_lines = [
        "18 log_b.txt",
        "52 log_d.txt"
    ]

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert lines == expected_lines, f"Manifest content is incorrect. Expected {expected_lines}, got {lines}"

def test_archive_content():
    archive_path = '/home/user/archive.bin'
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."

    with open(archive_path, 'rb') as f:
        content = f.read()

    expected_content = b"Warning: Low disk space.Error code 0x88F."
    assert content == expected_content, f"Archive content is incorrect. Expected {expected_content}, got {content}"