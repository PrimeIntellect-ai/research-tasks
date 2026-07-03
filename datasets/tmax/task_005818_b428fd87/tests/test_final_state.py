# test_final_state.py

import os
import json
import struct
import pytest

CONFIGS_DIR = "/home/user/configs"
WAL_FILE = "/home/user/tracker.wal"
SYMLINK_FILE = "/home/user/latest.elf"

def get_elf64_entry_point(filepath):
    """Extracts the e_entry field from an ELF64 binary."""
    with open(filepath, "rb") as f:
        e_ident = f.read(16)
        assert e_ident[:4] == b"\x7fELF", f"File {filepath} is not a valid ELF."
        # Check if it's 64-bit (class = 2)
        assert e_ident[4] == 2, f"File {filepath} is not a 64-bit ELF."

        # Read e_type (2), e_machine (2), e_version (4) -> 8 bytes total
        f.read(8)

        # Read e_entry (8 bytes)
        e_entry_bytes = f.read(8)

        # Data encoding: 1 = little endian, 2 = big endian
        endian = "<" if e_ident[5] == 1 else ">"

        e_entry = struct.unpack(f"{endian}Q", e_entry_bytes)[0]
        return e_entry

def get_expected_updates():
    """Parses JSON metadata and sorts by timestamp."""
    updates = []
    for filename in os.listdir(CONFIGS_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(CONFIGS_DIR, filename)
            with open(filepath, "r") as f:
                data = json.load(f)
                updates.append(data)

    # Sort by timestamp ascending
    updates.sort(key=lambda x: x["timestamp"])
    return updates

def test_wal_file_exists_and_correct():
    assert os.path.exists(WAL_FILE), f"WAL file {WAL_FILE} does not exist."
    assert os.path.isfile(WAL_FILE), f"{WAL_FILE} is not a regular file."

    updates = get_expected_updates()
    assert len(updates) > 0, "No JSON updates found to verify against."

    expected_lines = []
    for update in updates:
        config_id = update["config_id"]
        binary = update["binary"]
        binary_path = os.path.join(CONFIGS_DIR, binary)

        entry_point = get_elf64_entry_point(binary_path)
        hex_entry = hex(entry_point)  # hex() naturally strips leading zeros and adds '0x'

        expected_lines.append(f"{config_id},{binary},{hex_entry}")

    with open(WAL_FILE, "r") as f:
        actual_content = f.read().strip()

    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in WAL file, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"WAL line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"

def test_symlink_correct():
    assert os.path.islink(SYMLINK_FILE), f"{SYMLINK_FILE} does not exist or is not a symlink."

    updates = get_expected_updates()
    assert len(updates) > 0, "No JSON updates found to determine symlink target."

    last_binary = updates[-1]["binary"]
    expected_target = os.path.join(CONFIGS_DIR, last_binary)

    actual_target = os.readlink(SYMLINK_FILE)

    assert actual_target == expected_target, f"Symlink {SYMLINK_FILE} points to {actual_target}, expected {expected_target}."