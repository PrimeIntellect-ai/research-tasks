# test_final_state.py

import os
import glob
import gzip
import pytest

def test_utf16_csv_exists_and_valid():
    csv_path = "/home/user/chunks/index_utf16.csv"
    assert os.path.exists(csv_path), f"Expected file {csv_path} does not exist."

    try:
        with open(csv_path, 'rb') as f:
            content = f.read()
            text = content.decode('utf-16le')
    except Exception as e:
        pytest.fail(f"Failed to decode {csv_path} as UTF-16LE: {e}")

    assert 'chunk_name,num_frames,compressed_bytes' in text, "CSV header is missing or incorrect."

def test_chunks_exist_and_valid_gzip():
    chunks_dir = "/home/user/chunks"
    chunks = glob.glob(os.path.join(chunks_dir, "chunk_*.gz"))
    assert chunks, f"No chunk files found in {chunks_dir}."

    for chunk in chunks:
        try:
            with gzip.open(chunk, 'rb') as f:
                f.read()
        except Exception as e:
            pytest.fail(f"Chunk {chunk} is not a valid gzip file: {e}")

def test_latest_symlink_exists():
    symlink_path = "/home/user/chunks/latest.gz"
    assert os.path.islink(symlink_path), f"Expected symlink at {symlink_path} is missing or not a symlink."

def test_compression_metric_threshold():
    chunks_dir = "/home/user/chunks"
    chunks = glob.glob(os.path.join(chunks_dir, "chunk_*.gz"))
    assert chunks, f"No chunk files found in {chunks_dir}."

    total_size = sum(os.path.getsize(chunk) for chunk in chunks)
    threshold = 1500000

    assert total_size <= threshold, f"Total compressed size {total_size} bytes exceeds the threshold of {threshold} bytes. Ensure max compression (level 9) is used."