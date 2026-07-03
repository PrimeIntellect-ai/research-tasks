# test_final_state.py

import os
import glob
import bz2
import gzip
import pytest

def get_legacy_backups():
    base = "/home/user/legacy_archive"
    if not os.path.isdir(base):
        return []
    return [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]

def test_new_archive_structure():
    """Test that the required directories and files exist in the new archive."""
    backups = get_legacy_backups()
    assert backups, "No legacy backups found to test against."
    for b in backups:
        new_dir = f"/home/user/new_archive/{b}"
        assert os.path.isdir(new_dir), f"Missing new archive directory: {new_dir}"

        header_file = f"{new_dir}/header.bin"
        assert os.path.isfile(header_file), f"Missing header.bin in {new_dir}"

        chunks_dir = f"{new_dir}/chunks"
        assert os.path.isdir(chunks_dir), f"Missing chunks directory in {new_dir}"

        chunks = glob.glob(f"{chunks_dir}/part_*")
        assert len(chunks) > 0, f"No part_* chunks found in {chunks_dir}"

def test_headers_extracted_correctly():
    """Test that the 8-byte binary header was correctly extracted."""
    backups = get_legacy_backups()
    for b in backups:
        legacy_chunks = sorted(glob.glob(f"/home/user/legacy_archive/{b}/chunk_*"))
        assert legacy_chunks, f"No legacy chunks for {b}"

        with open(legacy_chunks[0], 'rb') as f:
            expected_header = f.read(8)

        header_path = f"/home/user/new_archive/{b}/header.bin"
        with open(header_path, 'rb') as f:
            actual_header = f.read()

        assert actual_header == expected_header, (
            f"Header mismatch for {b}. Expected {expected_header.hex()}, got {actual_header.hex()}"
        )

def test_chunk_sizes():
    """Test that all new chunks (except possibly the last one) are exactly 50KB."""
    backups = get_legacy_backups()
    for b in backups:
        chunks = sorted(glob.glob(f"/home/user/new_archive/{b}/chunks/part_*"))
        assert chunks, f"No new chunks found for {b}"

        # Check all but the last chunk
        for chunk in chunks[:-1]:
            size = os.path.getsize(chunk)
            assert size == 50 * 1024, f"Chunk {chunk} size is {size} bytes, expected exactly 51200 bytes."

def test_payload_transformation():
    """Test that the payload was correctly decompressed, transformed, and re-compressed."""
    backups = get_legacy_backups()
    for b in backups:
        # Reconstruct legacy payload
        legacy_chunks = sorted(glob.glob(f"/home/user/legacy_archive/{b}/chunk_*"))
        legacy_data = bytearray()
        for c in legacy_chunks:
            with open(c, 'rb') as f:
                legacy_data.extend(f.read())

        header = legacy_data[:8]
        expected_hex = header.hex().lower()

        try:
            original_text = gzip.decompress(legacy_data[8:])
        except Exception as e:
            pytest.fail(f"Failed to decompress legacy gzip payload for {b}: {e}")

        # Reconstruct new payload
        new_chunks = sorted(glob.glob(f"/home/user/new_archive/{b}/chunks/part_*"))
        new_data = bytearray()
        for c in new_chunks:
            with open(c, 'rb') as f:
                new_data.extend(f.read())

        try:
            new_text = bz2.decompress(new_data)
        except Exception as e:
            pytest.fail(f"Failed to decompress new bzip2 payload for {b}: {e}")

        # Verify transformation
        expected_suffix = f"\nVERIFIED: {expected_hex}".encode('utf-8')

        assert new_text.endswith(expected_suffix), (
            f"New payload for {b} does not end with the expected VERIFIED line: 'VERIFIED: {expected_hex}'"
        )

        assert new_text == original_text + expected_suffix, (
            f"The original payload for {b} was altered incorrectly or data is missing."
        )