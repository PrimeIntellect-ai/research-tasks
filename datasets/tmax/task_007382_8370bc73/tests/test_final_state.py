# test_final_state.py
import os
import json
import tarfile
import pytest

def test_processed_dataset_directory():
    assert os.path.isdir("/home/user/processed_dataset"), "Directory /home/user/processed_dataset/ is missing."

def test_compressed_files_exist():
    assert os.path.isfile("/home/user/processed_dataset/item1.gcode.cz"), "File item1.gcode.cz is missing."
    assert os.path.isfile("/home/user/processed_dataset/item3.gcode.cz"), "File item3.gcode.cz is missing."
    # Ensure item2 and notes are not processed
    assert not os.path.isfile("/home/user/processed_dataset/item2.gcode.cz"), "item2.gcode.cz should not exist (wrong material)."
    assert not os.path.isfile("/home/user/processed_dataset/notes.txt.cz"), "notes.txt.cz should not exist (not a .gcode file)."

def test_compressed_file_contents():
    with open("/home/user/processed_dataset/item1.gcode.cz", "r") as f:
        content1 = f.read()
    expected1 = "; Material: PETG\nG1 X100.0*3 Y200.0*3 Z1.0*3\nM104 S230\n"
    assert content1 == expected1, "item1.gcode.cz content does not match the expected custom compression."

    with open("/home/user/processed_dataset/item3.gcode.cz", "r") as f:
        content3 = f.read()
    expected3 = "; Material: PETG\n;*4 Custom header\nG0 F30*3\n"
    assert content3 == expected3, "item3.gcode.cz content does not match the expected custom compression."

def test_summary_json():
    summary_path = "/home/user/processed_dataset/summary.json"
    assert os.path.isfile(summary_path), "summary.json is missing."
    with open(summary_path, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json is not a valid JSON file.")

    assert "item1.gcode" in summary, "item1.gcode missing from summary.json"
    assert summary["item1.gcode"] == 55, "item1.gcode size is incorrect in summary.json"

    assert "item3.gcode" in summary, "item3.gcode missing from summary.json"
    assert summary["item3.gcode"] == 45, "item3.gcode size is incorrect in summary.json"

def test_final_archive():
    archive_path = "/home/user/final_archive.tar.gz"
    assert os.path.isfile(archive_path), "final_archive.tar.gz is missing."
    assert tarfile.is_tarfile(archive_path), "final_archive.tar.gz is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        basenames = [os.path.basename(n) for n in names]
        assert "item1.gcode.cz" in basenames, "item1.gcode.cz missing from archive."
        assert "item3.gcode.cz" in basenames, "item3.gcode.cz missing from archive."
        assert "summary.json" in basenames, "summary.json missing from archive."

        # Check that they are under a processed_dataset directory
        has_processed_dir = any("processed_dataset" in n for n in names)
        assert has_processed_dir, "Archive does not contain the processed_dataset directory structure."