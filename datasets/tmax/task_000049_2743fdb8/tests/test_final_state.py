# test_final_state.py

import os
import tarfile
import pytest

def test_c_program_exists():
    assert os.path.isfile("/home/user/queue_parser.c"), "C program /home/user/queue_parser.c is missing."

def test_targets_txt():
    targets_file = "/home/user/targets.txt"
    assert os.path.isfile(targets_file), f"{targets_file} is missing."

    with open(targets_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_paths = {"/home/user/data/dir_alpha", "/home/user/data/dir_gamma"}
    actual_paths = set(lines)

    assert actual_paths == expected_paths, f"Expected {targets_file} to contain exactly {expected_paths}, but found {actual_paths}"
    assert len(lines) == len(expected_paths), f"{targets_file} contains duplicates or extra lines."

def test_tar_archive():
    archive_file = "/home/user/required_backups.tar.gz"
    assert os.path.isfile(archive_file), f"Archive {archive_file} is missing."
    assert tarfile.is_tarfile(archive_file), f"{archive_file} is not a valid tar archive."

    with tarfile.open(archive_file, "r:gz") as tar:
        names = tar.getnames()

    # Check that alpha and gamma are in the archive
    has_alpha = any("dir_alpha" in name for name in names)
    has_gamma = any("dir_gamma" in name for name in names)

    assert has_alpha, "dir_alpha is missing from the tar archive."
    assert has_gamma, "dir_gamma is missing from the tar archive."

    # Check that beta and delta are NOT in the archive
    has_beta = any("dir_beta" in name for name in names)
    has_delta = any("dir_delta" in name for name in names)

    assert not has_beta, "dir_beta should NOT be in the tar archive."
    assert not has_delta, "dir_delta should NOT be in the tar archive."