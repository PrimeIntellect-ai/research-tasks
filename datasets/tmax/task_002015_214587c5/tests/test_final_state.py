# test_final_state.py

import os
import tarfile
import csv
import hashlib
import subprocess
import pytest

PROCESSED_DIR = "/home/user/titan_processed"
GCODE_DIR = os.path.join(PROCESSED_DIR, "gcode")
FIRMWARE_DIR = os.path.join(PROCESSED_DIR, "firmware")
MANIFEST_FILE = os.path.join(PROCESSED_DIR, "elf_manifest.csv")
FINAL_TAR = "/home/user/titan_final.tar.gz"
FINAL_SHA = "/home/user/titan_final.sha256"

def get_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()

def get_readelf_machine(filepath):
    try:
        output = subprocess.check_output(['readelf', '-h', filepath], text=True)
        for line in output.splitlines():
            if 'Machine:' in line:
                return line.split('Machine:')[1].strip()
    except Exception:
        pass
    return None

def test_gcode_files_renamed_and_moved():
    assert os.path.isdir(GCODE_DIR), f"{GCODE_DIR} is missing."

    expected_files = {
        "Main_Bracket.gcode": "A-101",
        "Drive_Gear.gcode": "B-202",
        "Sensor_Housing.gcode": "C-303"
    }

    for filename, asset_id in expected_files.items():
        filepath = os.path.join(GCODE_DIR, filename)
        assert os.path.isfile(filepath), f"Expected GCode file {filepath} not found."

        with open(filepath, 'r') as f:
            first_line = f.readline().strip()
            assert asset_id in first_line, f"{filepath} does not contain the expected AssetID {asset_id} in the first line."

def test_firmware_files_moved():
    assert os.path.isdir(FIRMWARE_DIR), f"{FIRMWARE_DIR} is missing."

    for filename in ["controller.elf", "sensor.elf"]:
        filepath = os.path.join(FIRMWARE_DIR, filename)
        assert os.path.isfile(filepath), f"Expected ELF file {filepath} not found."

def test_elf_manifest():
    assert os.path.isfile(MANIFEST_FILE), f"Manifest file {MANIFEST_FILE} is missing."

    with open(MANIFEST_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 3, "Manifest CSV does not have enough rows."
    assert rows[0] == ["Filename", "Machine", "SHA256"], "Manifest header is incorrect."

    manifest_data = {row[0]: {"machine": row[1], "sha256": row[2]} for row in rows[1:] if len(row) == 3}

    for filename in ["controller.elf", "sensor.elf"]:
        assert filename in manifest_data, f"{filename} missing from manifest."
        filepath = os.path.join(FIRMWARE_DIR, filename)

        actual_sha = get_sha256(filepath)
        actual_machine = get_readelf_machine(filepath)

        assert manifest_data[filename]["sha256"] == actual_sha, f"SHA256 mismatch for {filename} in manifest."
        assert manifest_data[filename]["machine"] == actual_machine, f"Machine value mismatch for {filename} in manifest."

def test_final_tarball():
    assert os.path.isfile(FINAL_TAR), f"Final tarball {FINAL_TAR} is missing."

    with tarfile.open(FINAL_TAR, "r:gz") as tar:
        names = tar.getnames()
        # Check that the root directory is titan_processed
        assert any(name.startswith("titan_processed") for name in names), "Tarball does not contain titan_processed/ directory."

def test_final_sha256():
    assert os.path.isfile(FINAL_SHA), f"Checksum file {FINAL_SHA} is missing."

    actual_hash = get_sha256(FINAL_TAR)
    expected_content = f"{actual_hash}  titan_final.tar.gz"

    with open(FINAL_SHA, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"Checksum file content is incorrect. Expected '{expected_content}', got '{content}'."