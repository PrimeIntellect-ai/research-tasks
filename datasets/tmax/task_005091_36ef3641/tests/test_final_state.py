# test_final_state.py
import os
import pytest

def test_quarantine_files():
    quarantine_dir = "/home/user/quarantine"
    assert os.path.isdir(quarantine_dir), "Quarantine directory does not exist."

    expected_files = ["corrupt_data.tar.gz", "bad_archive.zip"]
    for f in expected_files:
        file_path = os.path.join(quarantine_dir, f)
        assert os.path.isfile(file_path), f"Corrupt file {f} is not in quarantine."

def test_curated_artifacts_elf_x86():
    dir_path = "/home/user/curated_artifacts/ELF/Advanced_Micro_Devices_X86-64"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    file_path = os.path.join(dir_path, "app_x86.tar.gz")
    assert os.path.isfile(file_path), f"File app_x86.tar.gz is not in {dir_path}."

def test_curated_artifacts_elf_arm():
    dir_path = "/home/user/curated_artifacts/ELF/ARM"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    file_path = os.path.join(dir_path, "firmware_arm.zip")
    assert os.path.isfile(file_path), f"File firmware_arm.zip is not in {dir_path}."

def test_curated_artifacts_gcode_abs():
    dir_path = "/home/user/curated_artifacts/GCode/ABS"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    file_path = os.path.join(dir_path, "model_abs.tar.gz")
    assert os.path.isfile(file_path), f"File model_abs.tar.gz is not in {dir_path}."

def test_curation_log():
    log_path = "/home/user/curation.log"
    assert os.path.isfile(log_path), "Curation log file does not exist."

    with open(log_path, "r") as f:
        log_contents = f.read()

    expected_lines = [
        "[VALID] app_x86.tar.gz - ELF - Advanced_Micro_Devices_X86-64",
        "[VALID] firmware_arm.zip - ELF - ARM",
        "[VALID] model_abs.tar.gz - GCode - ABS",
        "[CORRUPT] corrupt_data.tar.gz - UNKNOWN - N/A",
        "[CORRUPT] bad_archive.zip - UNKNOWN - N/A"
    ]

    for line in expected_lines:
        assert line in log_contents, f"Expected log line '{line}' not found in {log_path}."