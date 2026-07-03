# test_final_state.py

import os
import re
import pytest

CONFIG_ROOT = "/home/user/config_root"
BACKUP_FILE = "/home/user/backup.ccf"
MANIFEST_FILE = "/home/user/manifest.log"
SCRIPT_FILE = "/home/user/backup_manager.py"

def compute_rle(text: str) -> str:
    if not text:
        return ""
    result = []
    current_char = text[0]
    count = 1
    for char in text[1:]:
        if char == current_char:
            count += 1
            if count == 10:
                result.append(f"9{current_char}")
                count = 1
        else:
            result.append(f"{count}{current_char}")
            current_char = char
            count = 1
    result.append(f"{count}{current_char}")
    return "".join(result)

def test_output_files_exist():
    """Test that the expected output files were created."""
    assert os.path.isfile(BACKUP_FILE), f"Backup file not found at {BACKUP_FILE}"
    assert os.path.isfile(MANIFEST_FILE), f"Manifest file not found at {MANIFEST_FILE}"

def test_manifest_content():
    """Test that the manifest contains the correct files and sizes."""
    expected_files = {
        "app.conf": 19,
        "db.conf": 25,
        "sub_dir/pad.conf": 24,
        "sub_dir/service.conf": 20
    }

    with open(MANIFEST_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    actual_files = {}
    for line in lines:
        parts = line.split(":")
        assert len(parts) == 2, f"Invalid manifest line format: {line}"
        rel_path = parts[0].strip()
        size = int(parts[1].strip())
        actual_files[rel_path] = size

    # Allow app_link.conf to be either skipped or resolved to app.conf
    # The requirement is deduplication of uniquely discovered files.
    if "app_link.conf" in actual_files and "app.conf" not in actual_files:
        actual_files["app.conf"] = actual_files.pop("app_link.conf")

    assert actual_files == expected_files, f"Manifest content mismatch. Expected {expected_files}, got {actual_files}"

def test_backup_content():
    """Test that the backup file contains the correct headers and RLE compressed data."""
    # Recompute expected content based on truth
    files_expected = {
        "app.conf": "server_name=app;   ",
        "db.conf": "host=127.0.0.1;port=5432;",
        "sub_dir/pad.conf": "padding=xxxxxxxxxxxxxxx;",
        "sub_dir/service.conf": "mode=active;retry=3;"
    }

    expected_blocks = {}
    for rel_path, content in files_expected.items():
        expected_blocks[rel_path] = compute_rle(content)

    with open(BACKUP_FILE, "r") as f:
        backup_content = f.read()

    # Check each file block
    for rel_path, expected_rle in expected_blocks.items():
        header1 = f"---FILE: {rel_path}---"
        header2 = f"---FILE: app_link.conf---" if rel_path == "app.conf" else header1

        # Find header
        if header1 in backup_content:
            header = header1
        elif header2 in backup_content:
            header = header2
        else:
            pytest.fail(f"Missing header for {rel_path} in backup.ccf")

        # Extract the line immediately following the header
        lines = backup_content.splitlines()
        header_idx = lines.index(header)
        assert header_idx + 1 < len(lines), f"Missing data line after header {header}"

        actual_rle = lines[header_idx + 1]
        assert actual_rle == expected_rle, f"RLE mismatch for {rel_path}. Expected '{expected_rle}', got '{actual_rle}'"

def test_script_source_requirements():
    """Test that the script uses mmap and atomic writes (rename/replace)."""
    assert os.path.isfile(SCRIPT_FILE), f"Script missing at {SCRIPT_FILE}"

    with open(SCRIPT_FILE, "r") as f:
        source = f.read()

    assert "mmap" in source, "The script does not appear to use the 'mmap' module as required."

    atomic_write_pattern = re.compile(r'os\.(rename|replace)|shutil\.move')
    assert atomic_write_pattern.search(source), "The script does not appear to use atomic writes (os.rename, os.replace, or shutil.move)."