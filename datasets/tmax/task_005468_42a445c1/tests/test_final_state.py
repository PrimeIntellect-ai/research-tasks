# test_final_state.py

import os
import struct
import pytest

def test_archiver_files_exist():
    assert os.path.isfile("/home/user/archiver.c"), "Source file /home/user/archiver.c is missing."
    assert os.path.isfile("/home/user/archiver"), "Executable /home/user/archiver is missing."
    assert os.access("/home/user/archiver", os.X_OK), "/home/user/archiver is not executable."

def test_output_archive_format_and_contents():
    archive_path = "/home/user/output.archive"
    assert os.path.isfile(archive_path), f"Output archive {archive_path} is missing."

    with open(archive_path, "rb") as f:
        data = f.read()

    assert data.startswith(b"RLE_ARC\n"), "Archive does not start with the correct global header 'RLE_ARC\\n'."

    offset = 8
    archived_files = {}

    while offset < len(data):
        if offset + 2 > len(data):
            pytest.fail("Archive truncated while reading path length.")

        path_len = struct.unpack_from("<H", data, offset)[0]
        offset += 2

        if offset + path_len > len(data):
            pytest.fail("Archive truncated while reading path string.")

        path_bytes = data[offset:offset+path_len]
        path_str = path_bytes.decode('ascii', errors='replace')
        offset += path_len

        # Read RLE data
        decoded_content = bytearray()
        while True:
            if offset + 2 > len(data):
                pytest.fail(f"Archive truncated while reading RLE data for {path_str}.")

            count = data[offset]
            value = data[offset+1]
            offset += 2

            if count == 0 and value == 0:
                break

            if count == 0:
                pytest.fail(f"Invalid RLE count 0 (other than EOF marker) for {path_str}.")

            decoded_content.extend([value] * count)

        archived_files[path_str] = bytes(decoded_content)

    expected_files = {
        "project_alpha/file1.txt": b"AAAAABBBCC",
        "project_beta/file2.txt": b"Hello World!"
    }

    assert len(archived_files) == len(expected_files), f"Expected exactly {len(expected_files)} files in archive, found {len(archived_files)}."

    for expected_path, expected_content in expected_files.items():
        assert expected_path in archived_files, f"Expected file {expected_path} not found in archive."
        assert archived_files[expected_path] == expected_content, f"Decoded content for {expected_path} does not match expected."