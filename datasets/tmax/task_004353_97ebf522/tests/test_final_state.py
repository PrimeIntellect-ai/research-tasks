# test_final_state.py

import os
import struct
import math
import pytest

def test_output_bin_exists():
    """Test that the output binary file was created."""
    file_path = '/home/user/output.bin'
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. The Rust program may not have run or failed to create it."

def test_output_bin_content():
    """Test that the output binary file contains the correct projected data."""
    file_path = '/home/user/output.bin'
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    expected = [
        (1, 0.0, 1.5),
        (2, -0.5, -0.3),
        (3, 0.0, 0.0),
        (4, 2.0, 2.4)
    ]

    with open(file_path, 'rb') as f:
        data = f.read()

    assert len(data) == 48, f"Expected output.bin to be exactly 48 bytes, but got {len(data)} bytes."

    for i in range(4):
        chunk = data[i*12 : (i+1)*12]
        row_id, v1, v2 = struct.unpack('<Iff', chunk)
        exp_id, exp_v1, exp_v2 = expected[i]

        assert row_id == exp_id, f"Row {i+1} ID mismatch: expected {exp_id}, got {row_id}."
        assert math.isclose(v1, exp_v1, abs_tol=1e-5), f"Row {i+1} val1 mismatch: expected {exp_v1}, got {v1}."
        assert math.isclose(v2, exp_v2, abs_tol=1e-5), f"Row {i+1} val2 mismatch: expected {exp_v2}, got {v2}."