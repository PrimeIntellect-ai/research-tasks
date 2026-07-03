# test_final_state.py

import os
import tarfile
import pytest

def test_targets_file():
    targets_path = "/home/user/targets.txt"
    assert os.path.isfile(targets_path), f"{targets_path} does not exist."

    with open(targets_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert "libalpha.so" in lines, "libalpha.so is missing from targets.txt"
    assert "libgamma.so" in lines, "libgamma.so is missing from targets.txt"
    assert len(lines) == 2, f"targets.txt should contain exactly 2 lines, found {len(lines)}"

def test_binaries_patched():
    signature = b"\xDE\xAD\xBE\xEF\xCF\xFA\xED\xFE"
    null_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"

    # Check libalpha.so
    libalpha_path = "/home/user/artifacts/libalpha.so"
    assert os.path.isfile(libalpha_path), f"{libalpha_path} does not exist."
    with open(libalpha_path, "rb") as f:
        content = f.read()
    assert signature not in content, "Deprecated signature still found in libalpha.so"
    assert content.count(null_bytes) >= 1, "Null byte replacement not found in libalpha.so"

    # Check libgamma.so
    libgamma_path = "/home/user/artifacts/libgamma.so"
    assert os.path.isfile(libgamma_path), f"{libgamma_path} does not exist."
    with open(libgamma_path, "rb") as f:
        content = f.read()
    assert signature not in content, "Deprecated signature still found in libgamma.so"
    assert content.count(null_bytes) >= 2, "Expected 2 null byte replacements in libgamma.so"

def test_unpatched_binaries_untouched():
    signature = b"\xDE\xAD\xBE\xEF\xCF\xFA\xED\xFE"

    libbeta_path = "/home/user/artifacts/libbeta.so"
    assert os.path.isfile(libbeta_path)
    with open(libbeta_path, "rb") as f:
        content = f.read()
    assert signature not in content

    libdelta_path = "/home/user/artifacts/libdelta.so"
    assert os.path.isfile(libdelta_path)
    with open(libdelta_path, "rb") as f:
        content = f.read()
    assert signature not in content

def test_c_program_exists_and_uses_mmap():
    patcher_c_path = "/home/user/patcher.c"
    assert os.path.isfile(patcher_c_path), f"{patcher_c_path} does not exist."
    with open(patcher_c_path, "r") as f:
        content = f.read()
    assert "mmap" in content, "The C program does not appear to use mmap."

    patcher_bin_path = "/home/user/patcher"
    assert os.path.isfile(patcher_bin_path), f"{patcher_bin_path} does not exist."

def test_incremental_backup():
    tar_path = "/home/user/patch_incremental.tar"
    assert os.path.isfile(tar_path), f"{tar_path} does not exist."

    with tarfile.open(tar_path, "r") as tar:
        names = tar.getnames()

    # Check that only the modified files and the directory are in the tar
    file_names = [name for name in names if not name.endswith('/') and name != 'artifacts']

    assert any("libalpha.so" in name for name in file_names), "libalpha.so missing from incremental backup"
    assert any("libgamma.so" in name for name in file_names), "libgamma.so missing from incremental backup"
    assert not any("libbeta.so" in name for name in file_names), "libbeta.so should not be in the incremental backup"
    assert not any("libdelta.so" in name for name in file_names), "libdelta.so should not be in the incremental backup"

def test_backup_contents_logged():
    log_path = "/home/user/backup_contents.txt"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "libalpha.so" in content, "libalpha.so missing from backup_contents.txt"
    assert "libgamma.so" in content, "libgamma.so missing from backup_contents.txt"
    assert "libbeta.so" not in content, "libbeta.so should not be in backup_contents.txt"