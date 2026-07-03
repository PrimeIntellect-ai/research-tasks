# test_final_state.py

import os
import pytest

def compress_null_rle(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    n = len(data)
    while i < n:
        if data[i] == 0x00:
            count = 0
            while i < n and data[i] == 0x00 and count < 255:
                count += 1
                i += 1
            out.append(0xFF)
            out.append(count)
        elif data[i] == 0xFF:
            out.append(0xFF)
            out.append(0x00)
            i += 1
        else:
            out.append(data[i])
            i += 1
    return bytes(out)

def test_source_and_executable_exist():
    cpp_file = '/home/user/null_compressor.cpp'
    exe_file = '/home/user/null_compressor'

    assert os.path.exists(cpp_file), f"Source code {cpp_file} is missing."
    assert os.path.exists(exe_file), f"Executable {exe_file} is missing."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_tmp_file_does_not_exist():
    tmp_file = '/home/user/compressed.archive.tmp'
    assert not os.path.exists(tmp_file), f"Temporary file {tmp_file} should have been renamed or deleted."

def test_compressed_archive_content():
    raw_file = '/home/user/raw_data.bin'
    archive_file = '/home/user/compressed.archive'

    assert os.path.exists(raw_file), f"Raw data file {raw_file} is missing."
    assert os.path.exists(archive_file), f"Compressed archive {archive_file} is missing."

    with open(raw_file, 'rb') as f:
        raw_data = f.read()

    expected_data = compress_null_rle(raw_data)

    with open(archive_file, 'rb') as f:
        actual_data = f.read()

    assert actual_data == expected_data, "The contents of the compressed archive do not match the expected Null-Byte RLE output."