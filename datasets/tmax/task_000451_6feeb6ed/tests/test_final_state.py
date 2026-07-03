# test_final_state.py

import os
import re
import tarfile
import pytest

def test_watcher_script_exists():
    assert os.path.isfile("/home/user/fleet_watcher.py"), "fleet_watcher.py is missing."
    assert os.path.isfile("/home/user/ready.flag"), "ready.flag is missing."

def test_spool_directory_empty():
    spool_dir = "/home/user/spool"
    assert os.path.isdir(spool_dir), f"{spool_dir} is missing."
    files_in_spool = os.listdir(spool_dir)
    assert "print_job.gcode" not in files_in_spool, "print_job.gcode was not removed from spool."
    assert "firmware_update.elf" not in files_in_spool, "firmware_update.elf was not removed from spool."

def test_archive_gcode_file():
    archive_path = "/home/user/archive/print_job.gcode.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} is missing."

    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."
    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()
        assert "print_job.gcode" in members, "print_job.gcode is missing from the tar archive."
        # Ensure it doesn't contain absolute paths
        assert "/home/user/spool/print_job.gcode" not in members, "Archive should not contain absolute paths."

def test_archive_elf_file():
    archive_path = "/home/user/archive/firmware_update.elf.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} is missing."

    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."
    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()
        assert "firmware_update.elf" in members, "firmware_update.elf is missing from the tar archive."
        # Ensure it doesn't contain absolute paths
        assert "/home/user/spool/firmware_update.elf" not in members, "Archive should not contain absolute paths."

def test_wal_log_contents():
    log_path = "/home/user/config_wal.log"
    assert os.path.isfile(log_path), f"WAL log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    gcode_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \| print_job\.gcode \| GCODE \| Ender_3_Pro$", re.MULTILINE)
    elf_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \| firmware_update\.elf \| ELF \| EM_X86_64$", re.MULTILINE)

    assert gcode_pattern.search(content), "WAL log is missing the correct entry for print_job.gcode."
    assert elf_pattern.search(content), "WAL log is missing the correct entry for firmware_update.elf."