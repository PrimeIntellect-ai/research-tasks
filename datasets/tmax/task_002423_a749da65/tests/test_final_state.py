# test_final_state.py
import os
import glob
import pytest

def test_renamed_gcode_files_exist():
    pla_file = "/home/user/files/PLA_4500s.gcode"
    petg_file = "/home/user/files/PETG_7200s.gcode"

    assert os.path.isfile(pla_file), f"Expected renamed file {pla_file} does not exist. Check gcode processing."
    assert os.path.isfile(petg_file), f"Expected renamed file {petg_file} does not exist. Check gcode processing."

def test_renamed_elf_files_exist():
    files_dir = "/home/user/files"
    elf_files = glob.glob(os.path.join(files_dir, "*.elf"))

    bit32_files = [f for f in elf_files if "32bit" in os.path.basename(f)]
    bit64_files = [f for f in elf_files if "64bit" in os.path.basename(f)]

    assert len(bit32_files) == 1, "Expected exactly one 32-bit ELF file renamed to firmware_32bit*.elf"
    assert len(bit64_files) == 1, "Expected exactly one 64-bit ELF file renamed to firmware_64bit*.elf"

def test_wal_log_exists_and_format():
    wal_file = "/home/user/rename_log.wal"
    assert os.path.isfile(wal_file), f"WAL log file {wal_file} does not exist."

    with open(wal_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 rename log entries, found {len(lines)}."

    # Check that each line follows the format [RENAME] <orig> -> <new>
    for line in lines:
        assert line.startswith("[RENAME] "), f"Log line does not start with '[RENAME] ': {line}"
        assert " -> " in line, f"Log line missing ' -> ' separator: {line}"

    # Check for specific original files
    log_content = "\n".join(lines)
    assert "part1.gcode -> PLA_4500s.gcode" in log_content, "Missing WAL entry for part1.gcode."
    assert "part2.gcode -> PETG_7200s.gcode" in log_content, "Missing WAL entry for part2.gcode."

    # Check for ELF files
    assert "fw_a.elf -> firmware_32bit" in log_content, "Missing WAL entry for fw_a.elf."
    assert "fw_b.elf -> firmware_64bit" in log_content, "Missing WAL entry for fw_b.elf."

def test_original_files_removed():
    orig_files = [
        "/home/user/files/part1.gcode",
        "/home/user/files/part2.gcode",
        "/home/user/files/fw_a.elf",
        "/home/user/files/fw_b.elf"
    ]
    for orig in orig_files:
        assert not os.path.exists(orig), f"Original file {orig} was not renamed/removed."