# test_final_state.py

import os
import pytest

def test_go_script_exists():
    """Verify that the Go program was created."""
    assert os.path.isfile("/home/user/sanitize.go"), "The Go program /home/user/sanitize.go is missing."

def test_master_log_exists_and_lines():
    """Verify master.log exists and has the correct number of lines."""
    master_log_path = "/home/user/processed/master.log"
    assert os.path.isfile(master_log_path), f"{master_log_path} is missing."

    with open(master_log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) == 120, f"Expected master.log to have 120 lines, but found {len(lines)}."

def test_chunks_exist_and_lines():
    """Verify the chunk files exist and have the correct number of lines."""
    chunks = {
        "chunk_00.log": 50,
        "chunk_01.log": 50,
        "chunk_02.log": 20
    }

    for chunk_name, expected_lines in chunks.items():
        chunk_path = f"/home/user/processed/{chunk_name}"
        # Some implementations might use alphabetic suffixes like xaa, xab, xac if standard split is used without -d,
        # but the prompt specifically says "named chunk_00.log, chunk_01.log, chunk_02.log".
        assert os.path.isfile(chunk_path), f"Expected chunk file {chunk_path} is missing."

        with open(chunk_path, "r") as f:
            lines = f.readlines()
        assert len(lines) == expected_lines, f"Expected {chunk_name} to have {expected_lines} lines, found {len(lines)}."

def test_redaction_and_counts():
    """Verify that the sensitive IP is redacted and replaced correctly."""
    master_log_path = "/home/user/processed/master.log"
    assert os.path.isfile(master_log_path), f"{master_log_path} is missing."

    with open(master_log_path, "r") as f:
        content = f.read()

    assert "192.168.1.100" not in content, "The sensitive IP '192.168.1.100' was found in master.log."

    redacted_count = content.count("[REDACTED_IP]")
    assert redacted_count == 90, f"Expected '[REDACTED_IP]' to appear 90 times, found {redacted_count} times."

def test_chunks_redaction():
    """Verify that the sensitive IP is not in any chunk."""
    chunks = ["chunk_00.log", "chunk_01.log", "chunk_02.log"]
    for chunk_name in chunks:
        chunk_path = f"/home/user/processed/{chunk_name}"
        if os.path.isfile(chunk_path):
            with open(chunk_path, "r") as f:
                content = f.read()
            assert "192.168.1.100" not in content, f"Sensitive IP found in {chunk_name}."