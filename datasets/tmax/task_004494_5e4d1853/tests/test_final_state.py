# test_final_state.py

import os
import struct
import pytest

def get_elf64_entry_point(filepath):
    """Parses the ELF64 header to extract the entry point."""
    with open(filepath, 'rb') as f:
        # e_ident is 16 bytes. Check magic number.
        e_ident = f.read(16)
        if e_ident[:4] != b'\x7fELF':
            raise ValueError(f"{filepath} is not an ELF file")
        if e_ident[4] != 2: # 2 = ELFCLASS64
            raise ValueError(f"{filepath} is not a 64-bit ELF")

        # e_type (2), e_machine (2), e_version (4) -> 8 bytes
        f.seek(24)
        # e_entry is 8 bytes
        entry_bytes = f.read(8)
        # Assuming little-endian for x86_64
        entry = struct.unpack('<Q', entry_bytes)[0]
        return entry

def test_recovered_archive_exists():
    assert os.path.exists("/home/user/recovered.tar.gz"), "/home/user/recovered.tar.gz is missing"

def test_binaries_extracted():
    binaries_dir = "/home/user/binaries"
    assert os.path.isdir(binaries_dir), f"{binaries_dir} directory is missing"
    for app in ["app_a", "app_b", "app_c"]:
        app_path = os.path.join(binaries_dir, app)
        assert os.path.isfile(app_path), f"Extracted binary {app} is missing in {binaries_dir}"

def test_c_program_exists():
    assert os.path.isfile("/home/user/analyze_elf.c"), "/home/user/analyze_elf.c is missing"
    assert os.path.isfile("/home/user/analyze_elf"), "Compiled executable /home/user/analyze_elf is missing"

def test_report_csv_correctness():
    report_path = "/home/user/report.csv"
    assert os.path.isfile(report_path), f"{report_path} is missing"

    expected_entries = []
    for app in ["app_a", "app_b", "app_c"]:
        src_path = f"/tmp/src/{app}"
        assert os.path.isfile(src_path), f"Original source binary {src_path} missing for ground truth"
        entry_point = get_elf64_entry_point(src_path)
        expected_entries.append(f"{app},{hex(entry_point)}")

    expected_entries.sort()

    with open(report_path, 'r') as f:
        # Read lines, strip whitespace, remove empty lines
        actual_entries = [line.strip() for line in f if line.strip()]

    # The requirement is that entries must be sorted alphabetically by filename
    assert actual_entries == expected_entries, (
        f"CSV contents mismatch.\nExpected:\n{expected_entries}\nGot:\n{actual_entries}"
    )