# test_final_state.py
import os
import pytest

def encode_rle(data: bytes) -> bytes:
    """Helper to generate expected RLE encoded data."""
    if not data:
        return b""
    result = bytearray()
    current_byte = data[0]
    count = 1
    for i in range(1, len(data)):
        if data[i] == current_byte and count < 255:
            count += 1
        else:
            result.append(current_byte)
            result.append(count)
            current_byte = data[i]
            count = 1
    result.append(current_byte)
    result.append(count)
    return bytes(result)

def test_ignored_files_exist():
    # Files that should NOT be processed must remain untouched
    access_dat = '/home/user/logs_archive/web/access.dat'
    small_log = '/home/user/logs_archive/db/small.log'

    assert os.path.exists(access_dat), f"Ignored file {access_dat} was incorrectly deleted."
    assert os.path.exists(small_log), f"Ignored file {small_log} was incorrectly deleted."

    # Verify contents remain the same
    with open(access_dat, 'rb') as f:
        assert f.read() == b'C' * 15000, f"Contents of {access_dat} were altered."
    with open(small_log, 'rb') as f:
        assert f.read() == b'D' * 10240, f"Contents of {small_log} were altered."

def test_processed_files_deleted():
    # Files that SHOULD be processed must be deleted after processing
    large1_log = '/home/user/logs_archive/web/large1.log'
    large2_log = '/home/user/logs_archive/db/large2.log'

    assert not os.path.exists(large1_log), f"Processed file {large1_log} was not deleted."
    assert not os.path.exists(large2_log), f"Processed file {large2_log} was not deleted."

def test_compressed_chunks_created():
    compressed_dir = '/home/user/compressed_logs'
    assert os.path.isdir(compressed_dir), f"Directory {compressed_dir} does not exist."

    expected_chunks = [
        'large1.log.chunk0.rle',
        'large1.log.chunk1.rle',
        'large1.log.chunk2.rle',
        'large2.log.chunk0.rle',
        'large2.log.chunk1.rle',
        'large2.log.chunk2.rle',
    ]

    for chunk in expected_chunks:
        chunk_path = os.path.join(compressed_dir, chunk)
        assert os.path.exists(chunk_path), f"Expected chunk file {chunk_path} is missing."

def test_rle_encoding_correctness():
    compressed_dir = '/home/user/compressed_logs'

    # Define the original raw data for each chunk
    chunk_data = {
        'large1.log.chunk0.rle': b'A' * 5120,
        'large1.log.chunk1.rle': b'B' * 5120,
        'large1.log.chunk2.rle': b'C' * 1760,
        'large2.log.chunk0.rle': b'X' * 5000 + b'Y' * 120,
        'large2.log.chunk1.rle': b'Y' * 4880 + b'Z' * 240,
        'large2.log.chunk2.rle': b'Z' * 4760,
    }

    for chunk_name, raw_data in chunk_data.items():
        chunk_path = os.path.join(compressed_dir, chunk_name)
        if not os.path.exists(chunk_path):
            pytest.fail(f"Cannot verify encoding because {chunk_path} is missing.")

        with open(chunk_path, 'rb') as f:
            actual_rle = f.read()

        expected_rle = encode_rle(raw_data)
        assert actual_rle == expected_rle, f"RLE encoding for {chunk_name} is incorrect."