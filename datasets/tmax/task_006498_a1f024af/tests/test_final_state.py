# test_final_state.py

import os
import tarfile
import pytest

def test_backup_exists_and_valid():
    """Test that the backup tarball exists and is a valid tar.gz file."""
    backup_path = "/home/user/backup/raw_archive.tar.gz"
    assert os.path.isfile(backup_path), f"Backup archive {backup_path} is missing."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # The tarball should contain printA.gcode and printB.gcode
            # They might be prefixed with the directory name, so we check for the filename.
            assert any(name.endswith("printA.gcode") for name in names), "printA.gcode not found in backup archive."
            assert any(name.endswith("printB.gcode") for name in names), "printB.gcode not found in backup archive."
    except tarfile.ReadError:
        pytest.fail(f"Backup archive {backup_path} is not a valid tar.gz file.")

def test_source_dir_empty():
    """Test that the source directory contains no .gcode files after processing."""
    source_dir = "/home/user/raw_gcode"
    assert os.path.isdir(source_dir), f"Source directory {source_dir} is missing."

    files = os.listdir(source_dir)
    gcode_files = [f for f in files if f.endswith(".gcode")]
    assert len(gcode_files) == 0, f"Source directory {source_dir} still contains .gcode files: {gcode_files}"

def test_processed_gcode_chunks():
    """Test that the processed GCode chunks exist, have the correct names, line counts, and are cleaned."""
    dest_dir = "/home/user/processed_gcode"
    assert os.path.isdir(dest_dir), f"Destination directory {dest_dir} is missing."

    expected_files = {
        "printA_part1.gcode": 50,
        "printA_part2.gcode": 50,
        "printA_part3.gcode": 10,
        "printB_part1.gcode": 40
    }

    actual_files = [f for f in os.listdir(dest_dir) if f.endswith(".gcode")]

    for expected_file, expected_lines in expected_files.items():
        assert expected_file in actual_files, f"Expected chunk {expected_file} is missing."

        filepath = os.path.join(dest_dir, expected_file)
        with open(filepath, "r") as f:
            lines = f.readlines()

        assert len(lines) == expected_lines, f"File {expected_file} has {len(lines)} lines, expected {expected_lines}."

        for line in lines:
            assert ";" not in line, f"Found comment in {expected_file}: {line.strip()}"
            assert line.strip() != "", f"Found empty line in {expected_file}"
            assert line == line.strip() + "\n", f"Line not stripped properly in {expected_file}: '{line}'"

    # Check for unexpected files
    unexpected_files = set(actual_files) - set(expected_files.keys())
    assert not unexpected_files, f"Found unexpected .gcode files in destination directory: {unexpected_files}"