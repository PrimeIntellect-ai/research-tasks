# test_final_state.py

import os
import zlib
import pytest

def test_libminiz_compiled():
    lib_path = "/app/miniz-3.0.2/libminiz.a"
    assert os.path.isfile(lib_path), f"The static library {lib_path} was not found. Did you compile miniz successfully?"

def test_organizer_cpp_exists():
    cpp_path = "/home/user/organizer.cpp"
    assert os.path.isfile(cpp_path), f"The source file {cpp_path} is missing."

def test_organized_bin_metric():
    bin_path = "/home/user/organized.bin"
    assert os.path.isfile(bin_path), f"The output file {bin_path} was not generated."

    size = os.path.getsize(bin_path)
    assert size <= 85000, (
        f"File size {size} is strictly greater than the threshold of 85000 bytes. "
        "Ensure you stripped timestamps, extracted 16-byte headers, and used MZ_BEST_COMPRESSION (level 9)."
    )

def test_organized_bin_is_valid_deflate():
    bin_path = "/home/user/organized.bin"
    if not os.path.isfile(bin_path):
        pytest.skip("Output file missing, cannot test compression validity.")

    with open(bin_path, "rb") as f:
        data = f.read()

    assert len(data) > 0, "The output file is empty."

    try:
        # Try standard zlib decompression (default for mz_compress)
        decompressed = zlib.decompress(data)
        assert len(decompressed) > 0, "Decompressed data is empty."
    except zlib.error as e1:
        try:
            # Try raw deflate decompression (in case they used a raw deflate init)
            decompressed = zlib.decompress(data, -15)
            assert len(decompressed) > 0, "Decompressed data is empty."
        except zlib.error as e2:
            pytest.fail(
                f"Failed to decompress {bin_path} as either standard zlib or raw deflate. "
                f"Is it properly compressed using miniz? (Errors: {e1}, {e2})"
            )