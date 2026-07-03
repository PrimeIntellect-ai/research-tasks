# test_final_state.py

import os
import pytest

def test_gcode_files_processed():
    original_gcode = '/home/user/backup_source/machine_1/part.gcode'
    assert not os.path.exists(original_gcode), f"Original GCode file {original_gcode} should have been deleted."

    part1 = f"{original_gcode}.part001"
    part2 = f"{original_gcode}.part002"
    part3 = f"{original_gcode}.part003"

    assert os.path.isfile(part1), f"Chunk file {part1} is missing."
    assert os.path.isfile(part2), f"Chunk file {part2} is missing."
    assert os.path.isfile(part3), f"Chunk file {part3} is missing."

    assert os.path.getsize(part1) == 100, f"{part1} should be exactly 100 bytes."
    assert os.path.getsize(part2) == 100, f"{part2} should be exactly 100 bytes."
    assert os.path.getsize(part3) == 45, f"{part3} should be exactly 45 bytes."

    # Reassemble and check content
    with open(part1, 'rb') as f1, open(part2, 'rb') as f2, open(part3, 'rb') as f3:
        content = f1.read() + f2.read() + f3.read()

    # The original file was repeated 5 times.
    # We expect UTF-8 encoding, stripped comments, and removed empty lines.
    expected_block = "M104 S200 \xb0C \nG28 \nG1 X10 Y10\nM109 S200 \nG1 Z0.2\n".encode('utf-8')
    expected_content = expected_block * 5

    assert content == expected_content, "The reassembled GCode content does not match the expected UTF-8 cleaned output."

def test_elf_files_renamed():
    old_service_orig = '/home/user/backup_source/system/bin/old_service'
    controller_orig = '/home/user/backup_source/machine_1/controller'

    assert not os.path.exists(old_service_orig), f"Original ELF file {old_service_orig} should have been renamed."
    assert not os.path.exists(controller_orig), f"Original ELF file {controller_orig} should have been renamed."

    old_service_bak = f"{old_service_orig}.elf.bak"
    controller_bak = f"{controller_orig}.elf.bak"

    assert os.path.isfile(old_service_bak), f"Renamed ELF file {old_service_bak} is missing."
    assert os.path.isfile(controller_bak), f"Renamed ELF file {controller_bak} is missing."

def test_manifest_log():
    manifest_path = '/home/user/manifest.log'
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    expected_lines = [
        "CHUNKED GCODE: machine_1/part.gcode.part001",
        "CHUNKED GCODE: machine_1/part.gcode.part002",
        "CHUNKED GCODE: machine_1/part.gcode.part003",
        "RENAMED ELF: machine_1/controller.elf.bak",
        "RENAMED ELF: system/bin/old_service.elf.bak"
    ]

    with open(manifest_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, "Manifest log contents do not match the expected sorted output."