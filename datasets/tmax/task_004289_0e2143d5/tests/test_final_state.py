# test_final_state.py
import os
import struct
import hashlib
import pytest

RAW_DATA_DIR = "/home/user/raw_data"
CATEGORIZED_DIR = "/home/user/categorized"
CPACK_PATH = "/home/user/dataset.cpack"

def get_expected_files():
    """
    Returns a dictionary of expected valid files, their types, and absolute paths.
    """
    expected = []
    for root, _, files in os.walk(RAW_DATA_DIR):
        for f in files:
            abs_path = os.path.join(root, f)
            with open(abs_path, 'rb') as file_obj:
                header = file_obj.read(16)

            if header.startswith(b'\x7F\x45\x4C\x46'):
                file_type = 'elf'
            elif header.startswith(b'\x37\x7F\x06\x82') or header.startswith(b'\x37\x7F\x06\x83'):
                file_type = 'wal'
            elif header.startswith(b'; FLAVOR:'):
                file_type = 'gcode'
            else:
                continue

            expected.append((abs_path, file_type))
    return expected

def test_symlinks_created_correctly():
    expected_files = get_expected_files()
    assert len(expected_files) > 0, "No valid files found in raw_data"

    for abs_path, file_type in expected_files:
        path_hash = hashlib.sha256(abs_path.encode('utf-8')).hexdigest()
        filename = os.path.basename(abs_path)
        symlink_name = f"{path_hash}_{filename}"
        symlink_path = os.path.join(CATEGORIZED_DIR, file_type, symlink_name)

        assert os.path.islink(symlink_path), f"Expected symlink missing or not a symlink: {symlink_path}"
        target = os.readlink(symlink_path)
        assert target == abs_path, f"Symlink {symlink_path} points to {target}, expected {abs_path}"

def test_cpack_archive_exists_and_valid():
    assert os.path.isfile(CPACK_PATH), f"Archive file not found: {CPACK_PATH}"

    with open(CPACK_PATH, 'rb') as f:
        header = f.read(8)
        assert header == b'CPACK\0\0\0', f"Invalid CPACK header: {header}"

        prev_path = ""
        entry_count = 0

        while True:
            len_bytes = f.read(2)
            if not len_bytes:
                break

            assert len(len_bytes) == 2, "Unexpected EOF reading path length"
            path_len = struct.unpack('<H', len_bytes)[0]

            path_bytes = f.read(path_len)
            assert len(path_bytes) == path_len, "Unexpected EOF reading path"
            path = path_bytes.decode('utf-8')

            assert path > prev_path, f"Paths are not lexicographically sorted: '{path}' came after '{prev_path}'"
            prev_path = path

            size_bytes = f.read(8)
            assert len(size_bytes) == 8, "Unexpected EOF reading uncompressed size"
            uncompressed_size = struct.unpack('<Q', size_bytes)[0]

            decoded = bytearray()
            while len(decoded) < uncompressed_size:
                pair = f.read(2)
                assert len(pair) == 2, "Unexpected EOF in RLE data"
                count, val = pair[0], pair[1]
                assert count > 0, "RLE count cannot be 0"
                decoded.extend([val] * count)

            assert len(decoded) == uncompressed_size, f"Decoded size mismatch for {path}"

            actual_path = os.path.join(CATEGORIZED_DIR, path)
            assert os.path.islink(actual_path), f"Path in archive does not point to a valid symlink: {actual_path}"

            with open(actual_path, 'rb') as orig:
                orig_data = orig.read()
                assert orig_data == decoded, f"Content mismatch for archived file {path}"

            entry_count += 1

        expected_count = len(get_expected_files())
        assert entry_count == expected_count, f"Archive contains {entry_count} files, expected {expected_count}"