# test_final_state.py

import os
import struct
import pytest

def test_c_file_exists():
    """Test that the C source code file exists."""
    c_file = "/home/user/extract_moves.c"
    assert os.path.exists(c_file), f"Source file {c_file} is missing."
    assert os.path.isfile(c_file), f"{c_file} is not a regular file."

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    executable = "/home/user/extract_moves"
    assert os.path.exists(executable), f"Executable {executable} is missing."
    assert os.path.isfile(executable), f"{executable} is not a regular file."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_output_file_exists_and_size():
    """Test that the binary output file exists and has the correct size."""
    output_file = "/home/user/datasets/combined_moves.bin"
    assert os.path.exists(output_file), f"Output file {output_file} is missing. Did you run the xargs command?"
    assert os.path.isfile(output_file), f"{output_file} is not a regular file."

    filesize = os.path.getsize(output_file)
    assert filesize == 48, f"Expected output file to be exactly 48 bytes, got {filesize} bytes."

def test_output_file_content():
    """Test that the binary output file contains the correct float pairs."""
    output_file = "/home/user/datasets/combined_moves.bin"
    assert os.path.exists(output_file), f"Output file {output_file} is missing."

    expected_pairs = {
        (1.0, 2.0),
        (3.0, 4.0),
        (-1.5, 10.0),
        (5.0, -2.5),
        (100.5, 200.5),
        (101.0, 201.0)
    }

    actual_pairs = set()
    filesize = os.path.getsize(output_file)
    assert filesize % 8 == 0, "File size is not a multiple of 8 bytes."

    num_pairs = filesize // 8
    with open(output_file, 'rb') as f:
        for _ in range(num_pairs):
            data = f.read(8)
            x, y = struct.unpack('ff', data)
            # Round slightly to handle floating point imprecision if necessary, 
            # but struct.pack/unpack of exact representable floats should match exactly.
            actual_pairs.add((round(x, 4), round(y, 4)))

    expected_pairs_rounded = {(round(x, 4), round(y, 4)) for x, y in expected_pairs}

    assert actual_pairs == expected_pairs_rounded, f"Extracted pairs do not match expected pairs.\nExpected: {expected_pairs_rounded}\nActual: {actual_pairs}"