# test_final_state.py

import os
import zipfile
import re
import pytest

ZIP_PATH = "/home/user/release_assets.zip"

def test_release_assets_zip_exists():
    """Test that the final zip archive was created."""
    assert os.path.exists(ZIP_PATH), f"The archive {ZIP_PATH} does not exist."
    assert os.path.isfile(ZIP_PATH), f"The path {ZIP_PATH} exists but is not a file."

def test_release_assets_zip_contents():
    """Test that the zip archive contains the correctly identified, filtered, and renamed files at its root."""
    assert os.path.exists(ZIP_PATH), f"Cannot check contents, {ZIP_PATH} is missing."

    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        namelist = zf.namelist()

        # Ensure files are at the root (no directory separators)
        for name in namelist:
            assert '/' not in name and '\\' not in name, f"File '{name}' is not at the root of the zip archive."

        # Check for the expected GCode file
        assert "gcode_Extruder_Gear.gcode" in namelist, "Missing or incorrect GCode file 'gcode_Extruder_Gear.gcode' in zip."

        # Check for the expected WAL file
        assert "database_j5k4l3m2.wal" in namelist, "Missing or incorrect WAL file 'database_j5k4l3m2.wal' in zip."

        # Check for the expected ELF file (architecture string can vary)
        elf_found = any(re.match(r"binary_[^_]+_a1b2c3d4\.elf$", name) for name in namelist)
        assert elf_found, "Missing or incorrectly named ELF file for 'a1b2c3d4' in zip. Expected format: binary_<architecture>_a1b2c3d4.elf"

        # Check that files modified on or after Jan 1, 2024 are excluded
        for name in namelist:
            assert "e5f6g7h8" not in name, f"Included file '{name}' which should have been filtered out by date (newer ELF)."
            assert "m1n2o3p4" not in name, f"Included file '{name}' which should have been filtered out by date (newer GCode)."

        # Check that exactly 3 files are present
        assert len(namelist) == 3, f"Expected exactly 3 files in zip, but found {len(namelist)}: {namelist}"