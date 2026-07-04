# test_final_state.py
import os
import struct
import pytest

def get_version(path):
    with open(path, 'rb') as f:
        header = f.read(4)
        if header != b'ARTF':
            return None
        ver_bytes = f.read(4)
        return struct.unpack('<I', ver_bytes)[0]

def test_backup_log_contents():
    log_file = "/home/user/backup.log"
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    with open(log_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 files to be logged, but found {len(lines)}: {lines}"

    expected_real_paths = {
        os.path.realpath("/home/user/artifacts/dirA/file_a.bin"),
        os.path.realpath("/home/user/artifacts/dirA/dirB/file_b.bin")
    }

    actual_real_paths = {os.path.realpath(p) for p in lines}
    assert actual_real_paths == expected_real_paths, (
        f"Logged paths do not resolve to the expected physical files.\n"
        f"Expected real paths: {expected_real_paths}\n"
        f"Actual real paths: {actual_real_paths}"
    )

def test_backup_dest_updated_files():
    # file_a.bin should be updated to version 5
    file_a_dest = "/home/user/backup_dest/dirA/file_a.bin"
    # It could also be under dirC/link_to_A/file_a.bin if traversed differently
    # Let's check the destination paths based on the log file to be robust
    log_file = "/home/user/backup.log"
    with open(log_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    for src_path in lines:
        rel_path = os.path.relpath(src_path, "/home/user/artifacts")
        dst_path = os.path.join("/home/user/backup_dest", rel_path)
        assert os.path.isfile(dst_path), f"Expected backed up file missing at: {dst_path}"

        src_ver = get_version(src_path)
        dst_ver = get_version(dst_path)
        assert dst_ver == src_ver, f"Destination file version {dst_ver} does not match source version {src_ver} for {dst_path}"

def test_backup_dest_untouched_files():
    # root_file.bin should remain version 2
    root_file = "/home/user/backup_dest/root_file.bin"
    assert os.path.isfile(root_file)
    assert get_version(root_file) == 2, "root_file.bin should not have been updated or altered"

    # file_c.bin should remain version 6
    file_c = "/home/user/backup_dest/dirC/file_c.bin"
    assert os.path.isfile(file_c)
    assert get_version(file_c) == 6, "file_c.bin should not have been overwritten (dest had higher version)"

def test_invalid_file_ignored():
    # invalid.bin should not be in backup_dest
    invalid_dest = "/home/user/backup_dest/invalid.bin"
    assert not os.path.exists(invalid_dest), "invalid.bin should have been ignored due to missing ARTF header"

def test_no_extra_files_in_dest():
    # Count the number of valid .bin files in backup_dest to ensure no unintended copies
    dest_dir = "/home/user/backup_dest"
    bin_count = 0
    for root, dirs, files in os.walk(dest_dir):
        for f in files:
            if f.endswith('.bin'):
                bin_count += 1

    # Expected files:
    # 1. root_file.bin
    # 2. dirC/file_c.bin
    # 3. file_a.bin (somewhere)
    # 4. file_b.bin (somewhere)
    assert bin_count == 4, f"Expected exactly 4 .bin files in backup_dest, found {bin_count}"