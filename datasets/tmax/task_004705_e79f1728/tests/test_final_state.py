# test_final_state.py
import os
import re
import math
import struct
import pytest

def test_dataset_stats_txt():
    """Check that dataset_stats.txt contains the correct max Z value."""
    stats_file = "/home/user/dataset_stats.txt"
    assert os.path.exists(stats_file), f"{stats_file} does not exist."

    with open(stats_file, "r") as f:
        content = f.read().strip()

    expected_str = "Max Z: 2.9155"
    assert expected_str in content, f"Expected '{expected_str}' in {stats_file}, but got '{content}'."

def test_dataset_visualization_png():
    """Check that dataset_visualization.png exists and is a valid PNG file."""
    img_file = "/home/user/dataset_visualization.png"
    assert os.path.exists(img_file), f"{img_file} does not exist."

    with open(img_file, "rb") as f:
        header = f.read(8)

    png_signature = b'\x89PNG\r\n\x1a\n'
    assert header == png_signature, f"{img_file} is not a valid PNG file based on its signature."

def test_normalized_dataset_npy():
    """Check the normalized_dataset.npy file for shape, mean, and std without third-party libraries."""
    npy_file = "/home/user/normalized_dataset.npy"
    assert os.path.exists(npy_file), f"{npy_file} does not exist."

    with open(npy_file, "rb") as f:
        magic = f.read(6)
        assert magic == b'\x93NUMPY', f"{npy_file} is not a valid .npy file."

        major, minor = struct.unpack('<BB', f.read(2))
        if major == 1:
            header_len = struct.unpack('<H', f.read(2))[0]
        elif major == 2:
            header_len = struct.unpack('<I', f.read(4))[0]
        else:
            pytest.fail(f"Unsupported .npy version: {major}")

        header_str = f.read(header_len).decode('ascii')

        # Check shape
        shape_match = re.search(r"'shape':\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)", header_str)
        assert shape_match is not None, "Could not parse shape from .npy header."
        rows, cols = int(shape_match.group(1)), int(shape_match.group(2))
        assert rows == 625 and cols == 3, f"Expected shape (625, 3), got ({rows}, {cols})."

        # Check descr
        descr_match = re.search(r"'descr':\s*'([^']+)'", header_str)
        assert descr_match is not None, "Could not parse descr from .npy header."
        descr = descr_match.group(1)

        data_bytes = f.read()

    # Parse floats
    if descr == '<f8':
        fmt = f'<{rows * cols}d'
        expected_bytes = rows * cols * 8
    elif descr == '<f4':
        fmt = f'<{rows * cols}f'
        expected_bytes = rows * cols * 4
    else:
        pytest.fail(f"Unsupported data type in .npy file: {descr}")

    assert len(data_bytes) >= expected_bytes, "Not enough data in .npy file."
    data_bytes = data_bytes[:expected_bytes]

    floats = struct.unpack(fmt, data_bytes)

    # Compute mean and std for each column
    for col in range(cols):
        col_data = [floats[r * cols + col] for r in range(rows)]
        mean = sum(col_data) / rows
        variance = sum((x - mean) ** 2 for x in col_data) / rows
        std = math.sqrt(variance)

        assert abs(mean) < 1e-3, f"Column {col} mean is {mean}, expected ~0.0"
        assert abs(std - 1.0) < 1e-3, f"Column {col} std is {std}, expected ~1.0"