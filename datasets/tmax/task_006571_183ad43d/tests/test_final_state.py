# test_final_state.py

import os
import pytest

DOCS_DIR = "/home/user/docs_project"

def test_parser_exists():
    cpp_file = "/home/user/parser.cpp"
    executable = "/home/user/parser"

    assert os.path.isfile(cpp_file), f"Source file {cpp_file} is missing."
    assert os.path.isfile(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_symlink_latest_elf():
    symlink_path = os.path.join(DOCS_DIR, "latest.elf")

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    target = os.readlink(symlink_path)
    # Could be absolute or relative, but the spec says "points to fw_v2.elf" usually meaning relative or the exact file
    # Let's check if it resolves to the correct file
    assert os.path.basename(target) == "fw_v2.elf", f"Symlink {symlink_path} does not point to fw_v2.elf."

def test_hardlink_model_backup():
    backup_path = os.path.join(DOCS_DIR, "model_backup.gcode")
    original_path = os.path.join(DOCS_DIR, "model_v2.gcode")

    assert os.path.exists(backup_path), f"Hard link {backup_path} does not exist."
    assert not os.path.islink(backup_path), f"{backup_path} should be a hard link, not a symlink."
    assert os.path.samefile(backup_path, original_path), f"{backup_path} does not point to the same inode as {original_path}."

def test_index_md_updated():
    index_md = os.path.join(DOCS_DIR, "index.md")
    assert os.path.exists(index_md), f"{index_md} does not exist."

    with open(index_md, "r") as f:
        content = f.read()

    assert "2438" in content, f"Expected print time '2438' not found in {index_md}. Content: {content}"
    assert "latest.elf" in content, f"Expected string 'latest.elf' not found in {index_md}. Content: {content}"
    assert "{{PRINT_TIME}}" not in content, f"Placeholder {{{{PRINT_TIME}}}} was not replaced."
    assert "{{LATEST_FIRMWARE}}" not in content, f"Placeholder {{{{LATEST_FIRMWARE}}}} was not replaced."