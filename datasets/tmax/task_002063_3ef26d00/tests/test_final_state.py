# test_final_state.py

import os
import tarfile
import pytest

GCODE_1_CONTENT = """G21 ; Set units to millimeters
G90 ; Use absolute coordinates
G1 X10 Y10 F1000
G1 Z0.5
G1 E5 F300
"""

GCODE_2_CONTENT = """M104 S200 ; Set extruder temp
M140 S60 ; Set bed temp
G28 ; Home all axes
G1 X100.5 Y100.5 Z10 F2000
"""

def test_extracted_gcode_directory_exists():
    """Verify that the extracted_gcode directory exists."""
    path = "/home/user/extracted_gcode"
    assert os.path.isdir(path), f"Directory {path} does not exist."

def test_part_base_gcode_content():
    """Verify that part_base.gcode was extracted and decompressed correctly."""
    path = "/home/user/extracted_gcode/part_base.gcode"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert content == GCODE_1_CONTENT, f"Content of {path} does not match expected output."

def test_heated_bed_init_gcode_content():
    """Verify that heated_bed_init.gcode was extracted and decompressed correctly."""
    path = "/home/user/extracted_gcode/heated_bed_init.gcode"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert content == GCODE_2_CONTENT, f"Content of {path} does not match expected output."

def test_tarball_exists_and_valid():
    """Verify that the tarball exists and contains the correct files."""
    tar_path = "/home/user/gcode_archive.tar.gz"
    assert os.path.isfile(tar_path), f"Archive {tar_path} does not exist."
    assert tarfile.is_tarfile(tar_path), f"Archive {tar_path} is not a valid tar file."

    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()
        # We check if the basenames of the files are in the archive
        basenames = [os.path.basename(name) for name in names]
        assert "part_base.gcode" in basenames, "part_base.gcode is missing from the tar archive."
        assert "heated_bed_init.gcode" in basenames, "heated_bed_init.gcode is missing from the tar archive."