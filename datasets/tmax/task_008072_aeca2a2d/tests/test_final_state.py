# test_final_state.py
import os
import struct
import pytest

def get_expected_files():
    """
    Derive the expected files to be archived based on the manifest and file system state.
    app_v1.bin was already archived.
    app_v3.bin and app_v4.bin are STALE and exist.
    missing.bin is STALE but does not exist.
    app_v2.bin is ACTIVE.
    """
    return [
        '/home/user/artifacts/binaries/app_v1.bin',
        '/home/user/artifacts/binaries/app_v3.bin',
        '/home/user/artifacts/binaries/app_v4.bin'
    ]

def test_archive_index_contents():
    index_path = '/home/user/archive_index.txt'
    assert os.path.isfile(index_path), f"Index file {index_path} is missing."

    with open(index_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = get_expected_files()
    assert len(lines) == len(expected), f"Expected {len(expected)} entries in index, found {len(lines)}."

    # Check that all expected files are in the index, preserving the required initial state
    assert lines[0] == expected[0], "The first entry in the index must remain app_v1.bin"
    assert set(lines) == set(expected), f"Index contents do not match expected stale files. Expected {expected}, got {lines}."

def test_stale_archive_binary_format():
    archive_path = '/home/user/stale_archive.bin'
    assert os.path.isfile(archive_path), f"Archive file {archive_path} is missing."

    expected_paths = get_expected_files()

    # Read the actual files from disk to know their exact sizes and contents
    expected_data = {}
    for path in expected_paths:
        with open(path, 'rb') as f:
            expected_data[path] = f.read()

    archived_paths = []

    with open(archive_path, 'rb') as f:
        while True:
            header = f.read(256)
            if not header:
                break

            assert len(header) == 256, "Archive header is not exactly 256 bytes."

            # Extract path
            path_bytes = header.rstrip(b'\x00')
            path_str = path_bytes.decode('utf-8')
            archived_paths.append(path_str)

            assert path_str in expected_data, f"Unexpected file path found in archive: {path_str}"

            # Read size
            size_data = f.read(8)
            assert len(size_data) == 8, f"Incomplete size header for {path_str}."
            size = struct.unpack('<Q', size_data)[0]

            expected_size = len(expected_data[path_str])
            assert size == expected_size, f"Size header for {path_str} is {size}, expected {expected_size}."

            # Read payload
            payload = f.read(size)
            assert len(payload) == size, f"Incomplete payload for {path_str}. Expected {size} bytes, got {len(payload)}."
            assert payload == expected_data[path_str], f"Payload data mismatch for {path_str}."

    assert archived_paths[0] == expected_paths[0], "The first archived file must remain app_v1.bin"
    assert set(archived_paths) == set(expected_paths), f"Archived paths do not match expected. Expected {expected_paths}, got {archived_paths}."

def test_scripts_exist():
    assert os.path.isfile('/home/user/find_stale.sh'), "Script /home/user/find_stale.sh is missing."
    assert os.access('/home/user/find_stale.sh', os.X_OK), "Script /home/user/find_stale.sh is not executable."

    assert os.path.isfile('/home/user/archiver.c'), "Source file /home/user/archiver.c is missing."
    assert os.path.isfile('/home/user/archiver'), "Compiled executable /home/user/archiver is missing."
    assert os.access('/home/user/archiver', os.X_OK), "Executable /home/user/archiver is not executable."