# test_final_state.py

import os
import tarfile
import tempfile
import subprocess
import pytest

ARCHIVE_PATH = "/home/user/organized_archive.tar.gz"
SOURCE_FILE = "/home/user/organizer.c"
BINARY_FILE = "/home/user/organizer"

def test_archive_exists():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive {ARCHIVE_PATH} is missing."

def test_archive_contents_and_structure():
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError as e:
            pytest.fail(f"Failed to extract tarball: {e}")

        base_extracted = os.path.join(tmpdir, "structured")
        assert os.path.isdir(base_extracted), "The archive must contain a 'structured' directory at its root."

        expected_files = {
            "elf/arch_62/controller.elf",
            "elf/arch_40/sensor.elf",
            "gcode/temp_215/chassis.gcode",
            "gcode/temp_190/bracket.gcode",
            "manifest.txt"
        }

        for rel_path in expected_files:
            full_path = os.path.join(base_extracted, rel_path)
            assert os.path.isfile(full_path), f"Expected file missing in archive: structured/{rel_path}"

        # Verify manifest contents
        manifest_path = os.path.join(base_extracted, "manifest.txt")
        with open(manifest_path, "r") as f:
            manifest_lines = [line.strip() for line in f.readlines() if line.strip()]

        expected_lines = {
            "controller.elf - ELF - arch 62",
            "sensor.elf - ELF - arch 40",
            "chassis.gcode - GCODE - temp 215",
            "bracket.gcode - GCODE - temp 190"
        }

        actual_lines = set(manifest_lines)
        missing_lines = expected_lines - actual_lines
        assert not missing_lines, f"Manifest is missing expected lines: {missing_lines}"

def test_organizer_binary_and_source_exist():
    assert os.path.isfile(SOURCE_FILE), f"Source file {SOURCE_FILE} is missing."
    assert os.path.isfile(BINARY_FILE), f"Binary file {BINARY_FILE} is missing."

def test_atomic_write_rename_used():
    assert os.path.isfile(SOURCE_FILE), "Source file is missing, cannot verify rename() usage."
    with open(SOURCE_FILE, "r") as f:
        source_code = f.read()

    # Check for rename() usage in the source code
    assert "rename(" in source_code.replace(" ", ""), "The C source code does not appear to use the rename() function for atomic writes."