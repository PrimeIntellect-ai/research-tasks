# test_final_state.py

import os
import struct
import pytest

def get_elf64_entry_point(filepath):
    """Extracts the entry point from a 64-bit ELF file using standard library."""
    with open(filepath, 'rb') as f:
        magic = f.read(4)
        if magic != b'\x7fELF':
            return None
        # Check if 64-bit
        ei_class = f.read(1)
        if ei_class != b'\x02':
            return None
        # 64-bit entry point is at offset 0x18
        f.seek(0x18)
        entry_bytes = f.read(8)
        entry_point = struct.unpack('<Q', entry_bytes)[0]
        return hex(entry_point)

def test_elf_parser_c_exists_and_contains_flock():
    path = "/home/user/elf_parser.c"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "flock" in content, f"{path} does not seem to use flock as required."

def test_elf_parser_executable():
    path = "/home/user/elf_parser"
    assert os.path.isfile(path), f"Compiled executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_curate_sh_executable():
    path = "/home/user/curate.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

def test_curation_report_content():
    report_path = "/home/user/curation_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in the report, found {len(lines)}."

    expected_ls_ep = get_elf64_entry_point("/home/user/artifacts/bin_ls")
    expected_cat_ep = get_elf64_entry_point("/home/user/artifacts/bin_cat")

    expected_ls_line = f"/home/user/artifacts/bin_ls : {expected_ls_ep}"
    expected_cat_line = f"/home/user/artifacts/bin_cat : {expected_cat_ep}"

    assert expected_ls_line in lines, f"Missing or incorrect entry for bin_ls. Expected: '{expected_ls_line}'"
    assert expected_cat_line in lines, f"Missing or incorrect entry for bin_cat. Expected: '{expected_cat_line}'"