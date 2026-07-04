# test_final_state.py

import os
import re
import subprocess

def test_no_zip_slip():
    hacked_file = "/home/user/system_conf/hacked.txt"
    assert not os.path.exists(hacked_file), f"Zip slip vulnerability exploited: {hacked_file} was extracted outside the target directory."

def test_valid_files_extracted():
    expected_files = [
        "/home/user/docs_target/firmware.elf",
        "/home/user/docs_target/calibration.gcode",
        "/home/user/docs_target/compile.log"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Valid file {f} was not properly extracted."

def test_release_summary_exists_and_format():
    summary_path = "/home/user/docs_target/release_summary.md"
    assert os.path.isfile(summary_path), f"Summary report {summary_path} is missing."

    with open(summary_path, "r") as f:
        content = f.read()

    # Verify GCode Max Extrusion
    assert "- calibration.gcode: Max Extrusion 6.8" in content, "GCode max extrusion for calibration.gcode is missing or incorrect in summary."

    # Verify FATAL block
    expected_fatal = "[2023-10-24] FATAL Linker error: out of memory\n  at module hardware_init.c:120\n  memory map exhausted"
    assert expected_fatal in content, "The exact FATAL log block is missing or incorrect in the summary."

    # Verify ELF Entry Point
    elf_path = "/home/user/docs_target/firmware.elf"
    entry_point = None
    if os.path.isfile(elf_path):
        try:
            output = subprocess.check_output(["readelf", "-h", elf_path], text=True)
            match = re.search(r"Entry point address:\s+(0x[0-9a-fA-F]+)", output)
            if match:
                entry_point = match.group(1).lower()
        except Exception:
            pass

    if entry_point:
        assert re.search(rf"- firmware\.elf: Entry Point {entry_point}", content.lower()), f"ELF entry point (expected {entry_point}) missing or incorrect in summary."
    else:
        assert re.search(r"- firmware\.elf: Entry Point 0x[0-9a-fA-F]+", content), "ELF entry point format missing in summary."