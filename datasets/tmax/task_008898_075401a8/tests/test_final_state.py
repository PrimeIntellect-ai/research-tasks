# test_final_state.py

import os
import pytest

CONFIGS_DIR = "/home/user/configs"
WAL_FILE = "/home/user/config.wal"
GO_FILE = "/home/user/config_extractor.go"
ESCAPED_FILE = "/home/user/escaped.conf"

def test_extracted_safe_files():
    """Check that safe files are extracted correctly."""
    assert os.path.isdir(CONFIGS_DIR), f"{CONFIGS_DIR} directory is missing."

    expected_files = ["app.conf", "db.conf", "safe_in_malicious.conf"]
    for f in expected_files:
        path = os.path.join(CONFIGS_DIR, f)
        assert os.path.isfile(path), f"Expected safe file {f} was not extracted to {CONFIGS_DIR}."

def test_prevented_zip_slip():
    """Check that the malicious file was not extracted."""
    # Should not be in configs dir
    escaped_in_configs = os.path.join(CONFIGS_DIR, "escaped.conf")
    assert not os.path.exists(escaped_in_configs), f"Malicious file was extracted to {escaped_in_configs}."

    # Should not be in the parent dir either
    assert not os.path.exists(ESCAPED_FILE), f"Zip slip vulnerability exploited! File found at {ESCAPED_FILE}."

def test_wal_file_contents():
    """Check that the WAL file contains the correct entries."""
    assert os.path.isfile(WAL_FILE), f"WAL file {WAL_FILE} is missing."

    with open(WAL_FILE, "r") as f:
        content = f.read()

    expected_entries = [
        "ENTRY: app.conf | STATUS: EXTRACTED",
        "ENTRY: db.conf | STATUS: EXTRACTED",
        "ENTRY: ../../user/escaped.conf | STATUS: SLIP_DETECTED",
        "ENTRY: safe_in_malicious.conf | STATUS: EXTRACTED"
    ]

    for entry in expected_entries:
        assert entry in content, f"Expected WAL entry not found: '{entry}'"

def test_go_code_exists_and_uses_flock():
    """Check that the Go source code exists and uses syscall.Flock."""
    assert os.path.isfile(GO_FILE), f"Go source file {GO_FILE} is missing."

    with open(GO_FILE, "r") as f:
        content = f.read()

    assert "syscall.Flock" in content, "Go program does not seem to use syscall.Flock."
    assert "syscall.LOCK_EX" in content, "Go program does not seem to use syscall.LOCK_EX."