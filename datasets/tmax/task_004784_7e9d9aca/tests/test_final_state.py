# test_final_state.py

import os
import zlib
import subprocess
import pytest

def get_elf_entry_point(filepath):
    """Uses readelf to find the entry point address of an ELF file."""
    result = subprocess.run(
        ["readelf", "-h", filepath],
        capture_output=True,
        text=True,
        check=True
    )
    for line in result.stdout.splitlines():
        if "Entry point address:" in line:
            # e.g., "  Entry point address:               0x401000"
            parts = line.split(":")
            if len(parts) == 2:
                return parts[1].strip().lower()
    raise ValueError(f"Could not find entry point in {filepath}")

def test_final_summary_exists_and_correct():
    zlib_path = "/home/user/final_summary.zlib"
    assert os.path.isfile(zlib_path), f"File {zlib_path} is missing."

    with open(zlib_path, "rb") as f:
        compressed_data = f.read()

    try:
        decompressed_data = zlib.decompress(compressed_data).decode("utf-8")
    except Exception as e:
        pytest.fail(f"Failed to decompress and decode {zlib_path}: {e}")

    # Dynamically determine the expected output
    fw1_entry = get_elf_entry_point("/home/user/project_files/firmware/fw1.elf")
    fw2_entry = get_elf_entry_point("/home/user/project_files/firmware/fw2.elf")

    expected_output = f"""[part1.gcode]
G0 X10 Y10 Z5 F1000 °C
G1 X15 Y15 Z0 F500
G1 X20 Y15 Z0
[part2.gcode]
G0 Z10
G0 X0 Y0
G1 Z-1 F100

fw1.elf: {fw1_entry}
fw2.elf: {fw2_entry}
"""

    assert decompressed_data.strip() == expected_output.strip(), (
        "Decompressed content does not match the expected output.\n"
        f"Expected:\n{expected_output}\n"
        f"Got:\n{decompressed_data}"
    )

def test_intermediate_files_exist():
    gcode_summary = "/home/user/gcode_summary.txt"
    elf_summary = "/home/user/elf_summary.txt"

    assert os.path.isfile(gcode_summary), f"File {gcode_summary} is missing."
    assert os.path.isfile(elf_summary), f"File {elf_summary} is missing."

    with open(gcode_summary, "r", encoding="utf-8") as f:
        gcode_content = f.read()

    assert "[part1.gcode]" in gcode_content, "gcode_summary.txt missing part1.gcode data"
    assert "G0 X10 Y10 Z5 F1000 °C" in gcode_content, "gcode_summary.txt missing UTF-8 decoded content"