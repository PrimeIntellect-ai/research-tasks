# test_final_state.py
import os
import struct
import hashlib
import glob
import pytest

FINAL_DOC_PATH = '/home/user/final_doc.md'
ASSETS_DIR = '/home/user/assets'
ELF_PATH = '/home/user/assets/firmware.elf'

def get_elf_entry_point(filepath):
    with open(filepath, 'rb') as f:
        # Read the e_ident to check if it's 64-bit
        e_ident = f.read(16)
        if e_ident[:4] != b'\x7fELF':
            raise ValueError("Not an ELF file")

        is_64_bit = e_ident[4] == 2
        endianness = '<' if e_ident[5] == 1 else '>'

        if is_64_bit:
            # e_entry is at offset 0x18 (24) and is 8 bytes long
            f.seek(24)
            entry_bytes = f.read(8)
            entry_point = struct.unpack(endianness + 'Q', entry_bytes)[0]
        else:
            # e_entry is at offset 0x18 (24) and is 4 bytes long
            f.seek(24)
            entry_bytes = f.read(4)
            entry_point = struct.unpack(endianness + 'I', entry_bytes)[0]

        return hex(entry_point)

def get_sha256sums():
    sums = []
    # Match shell expansion of /home/user/assets/*
    files = sorted(glob.glob(os.path.join(ASSETS_DIR, '*')))
    for filepath in files:
        if os.path.isfile(filepath):
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                hasher.update(f.read())
            sums.append(f"{hasher.hexdigest()}  {filepath}")
    return sums

def test_final_doc_exists():
    assert os.path.isfile(FINAL_DOC_PATH), f"The file {FINAL_DOC_PATH} does not exist."

def test_gcode_stats_replaced():
    with open(FINAL_DOC_PATH, 'r') as f:
        content = f.read()

    expected_str = "Max X: 120.5, Max Y: 110.0, Max Z: 15.0"
    assert expected_str in content, f"Expected GCode stats '{expected_str}' not found in final_doc.md."
    assert "{{GCODE_STATS" not in content, "GCODE_STATS placeholder was not removed."

def test_elf_entry_replaced():
    entry_point_hex = get_elf_entry_point(ELF_PATH)
    # Remove '0x' from python's hex() to format it manually if needed, 
    # but python's hex() already includes '0x' and lowercase hex
    expected_str = f"Entry Point: {entry_point_hex}"

    with open(FINAL_DOC_PATH, 'r') as f:
        content = f.read()

    assert expected_str in content, f"Expected ELF entry point '{expected_str}' not found in final_doc.md."
    assert "{{ELF_ENTRY" not in content, "ELF_ENTRY placeholder was not removed."

def test_manifest_appended():
    with open(FINAL_DOC_PATH, 'r') as f:
        content = f.read()

    assert "## Manifest" in content, "Manifest header '## Manifest' not found in final_doc.md."

    expected_sums = get_sha256sums()
    for s in expected_sums:
        assert s in content, f"Expected checksum line '{s}' not found in the manifest section of final_doc.md."