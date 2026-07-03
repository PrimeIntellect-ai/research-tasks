# test_final_state.py

import os
import difflib
import pytest

def test_server_config_similarity():
    """
    Test that the reconstructed server_config.ini matches the expected ground truth
    with a similarity ratio of at least 0.90.
    """
    expected = """[server]
port=8080
host=0.0.0.0
[database]
url=sqlite:///db.sqlite
redis_host=127.0.0.1"""

    config_path = "/home/user/server_config.ini"
    assert os.path.exists(config_path), f"The reconstructed configuration file is missing at {config_path}."
    assert os.path.isfile(config_path), f"The path {config_path} exists but is not a file."

    with open(config_path, "r") as f:
        actual = f.read().strip()

    ratio = difflib.SequenceMatcher(None, expected, actual).ratio()
    assert ratio >= 0.90, f"Similarity ratio {ratio:.4f} is below the threshold of 0.90.\nExpected:\n{expected}\n\nActual:\n{actual}"

def test_parsed_logs_chunks():
    """
    Test that the parsed logs have been split into chunk files of 5 records each.
    """
    chunks_dir = "/home/user/parsed_logs"
    assert os.path.exists(chunks_dir), f"The parsed logs directory is missing at {chunks_dir}."
    assert os.path.isdir(chunks_dir), f"The path {chunks_dir} is not a directory."

    chunk_files = sorted([f for f in os.listdir(chunks_dir) if f.startswith("chunk_") and f.endswith(".log")])
    assert len(chunk_files) > 0, f"No chunk files matching 'chunk_*.log' found in {chunks_dir}."

    # Check that the first chunk contains exactly 5 records
    first_chunk_path = os.path.join(chunks_dir, chunk_files[0])
    with open(first_chunk_path, "r") as f:
        content = f.read()

    start_count = content.count("START_RECORD")
    assert start_count == 5, f"Expected 5 records in {chunk_files[0]}, but found {start_count} 'START_RECORD' entries."