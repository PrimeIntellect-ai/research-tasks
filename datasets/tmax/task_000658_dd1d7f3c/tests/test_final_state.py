# test_final_state.py

import os
import glob
import re
import pytest

COMMITS_WAL_PATH = "/home/user/backups/processed/commits.wal"
CHUNKS_DIR = "/home/user/backups/processed/chunks"
RAW_LOGS_DIR = "/home/user/backups/raw_logs"

def get_expected_commits_content():
    """
    Dynamically parses the raw_logs directory to extract, filter, and sort
    the committed transactions as expected by the task.
    """
    wal_files = glob.glob(os.path.join(RAW_LOGS_DIR, "**", "*.wal"), recursive=True)

    transactions = []

    for wal_file in wal_files:
        with open(wal_file, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        current_tx = []
        tx_id = None
        for line in lines:
            if "BEGIN TX" in line:
                match = re.search(r"BEGIN TX (\d+)", line)
                if match:
                    tx_id = int(match.group(1))
                current_tx = [line]
            elif "COMMIT TX" in line:
                current_tx.append(line)
                if tx_id is not None:
                    transactions.append((tx_id, "\n".join(current_tx)))
                current_tx = []
                tx_id = None
            elif "ROLLBACK TX" in line:
                current_tx = []
                tx_id = None
            elif current_tx:
                current_tx.append(line)

    # Sort transactions by ID ascending
    transactions.sort(key=lambda x: x[0])

    # Join with a single empty line (\n\n) and ensure it ends with a newline
    if not transactions:
        return b""

    content_str = "\n\n".join(tx[1] for tx in transactions) + "\n"
    return content_str.encode("utf-8")

def test_commits_wal_content():
    assert os.path.isfile(COMMITS_WAL_PATH), f"File missing: {COMMITS_WAL_PATH}"

    with open(COMMITS_WAL_PATH, "rb") as f:
        actual_content = f.read()

    expected_content = get_expected_commits_content()

    assert actual_content == expected_content, (
        "The contents of commits.wal do not match the expected sorted, "
        "filtered transaction blocks separated by an empty line."
    )

def test_chunks_created_correctly():
    assert os.path.isdir(CHUNKS_DIR), f"Directory missing: {CHUNKS_DIR}"

    expected_content = get_expected_commits_content()
    expected_chunks = [expected_content[i:i+150] for i in range(0, len(expected_content), 150)]

    # Check that the correct number of chunks exists
    chunk_files = sorted(glob.glob(os.path.join(CHUNKS_DIR, "chunk_*.dat")))
    assert len(chunk_files) == len(expected_chunks), (
        f"Expected {len(expected_chunks)} chunk files, but found {len(chunk_files)}."
    )

    # Verify each chunk's content and naming
    for idx, expected_chunk_data in enumerate(expected_chunks):
        expected_filename = f"chunk_{idx:02d}.dat"
        expected_filepath = os.path.join(CHUNKS_DIR, expected_filename)

        assert os.path.isfile(expected_filepath), f"Expected chunk file missing: {expected_filepath}"

        with open(expected_filepath, "rb") as f:
            actual_chunk_data = f.read()

        assert actual_chunk_data == expected_chunk_data, (
            f"Content mismatch in {expected_filename}. "
            f"Expected {len(expected_chunk_data)} bytes, got {len(actual_chunk_data)} bytes."
        )