# test_final_state.py

import os
import gzip
import pytest

def test_clean_gz_size():
    """
    Test that the final compressed file exists and its size is within the target threshold.
    """
    filepath = '/home/user/clean.gz'
    assert os.path.exists(filepath), f"Output file does not exist: {filepath}"

    size = os.path.getsize(filepath)
    threshold = 250

    assert size <= threshold, f"Metric: {size}. Expected size <= {threshold} bytes. The file is too large, indicating failure to deduplicate or decode properly."

def test_clean_gz_validity():
    """
    Test that the final compressed file is a valid gzip archive and contains data.
    """
    filepath = '/home/user/clean.gz'
    assert os.path.exists(filepath), f"Output file does not exist: {filepath}"

    try:
        with gzip.open(filepath, 'rt') as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Failed to read {filepath} as a gzip file: {e}")

    assert len(content) > 0, "The decompressed file is empty, data recovery failed."