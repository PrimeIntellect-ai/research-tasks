# test_final_state.py

import os
import pytest

def test_compressor_script_exists_and_executable():
    script_path = "/home/user/compressor.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Expected script {script_path} to be executable."

def test_backup_bin_exists():
    backup_path = "/home/user/backup.bin"
    assert os.path.isfile(backup_path), f"Expected backup file {backup_path} does not exist."

def test_compression_ratio():
    backup_path = "/home/user/backup.bin"
    bin_b_path = "/home/user/repo/bin_B.dat"
    bin_c_path = "/home/user/repo/bin_C.dat"

    assert os.path.isfile(backup_path), f"Backup file {backup_path} is missing."
    assert os.path.isfile(bin_b_path), f"File {bin_b_path} is missing."
    assert os.path.isfile(bin_c_path), f"File {bin_c_path} is missing."

    raw_size = os.path.getsize(bin_b_path) + os.path.getsize(bin_c_path)
    compressed_size = os.path.getsize(backup_path)

    assert compressed_size > 0, "Backup file is empty."

    compression_ratio = raw_size / compressed_size
    threshold = 1.42

    assert compression_ratio >= threshold, (
        f"Compression ratio too low. "
        f"Raw size: {raw_size}, Compressed size: {compressed_size}. "
        f"Ratio: {compression_ratio:.3f}, Expected at least: {threshold}"
    )