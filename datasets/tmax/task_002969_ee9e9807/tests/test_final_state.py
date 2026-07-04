# test_final_state.py

import os
import subprocess
import tarfile
import pytest

def get_build_id(filepath):
    """Extract Build ID from an ELF file using readelf."""
    try:
        output = subprocess.check_output(['readelf', '-n', filepath], stderr=subprocess.DEVNULL, text=True)
        for line in output.splitlines():
            if "Build ID:" in line:
                return line.split("Build ID:")[1].strip()
    except Exception:
        pass
    return None

@pytest.fixture(scope="module")
def expected_files():
    source_files = {
        "ls_tool": "/bin/ls",
        "grep_tool": "/bin/grep",
        "cat_tool": "/bin/cat"
    }
    expected = []
    for orig_name, bin_path in source_files.items():
        build_id = get_build_id(bin_path)
        assert build_id is not None, f"Could not extract build ID from {bin_path}"
        expected.append(f"{orig_name}_{build_id}.elf")
    return sorted(expected)

def test_clean_backup_directory(expected_files):
    clean_backup_dir = "/home/user/clean_backup"
    assert os.path.isdir(clean_backup_dir), f"Directory {clean_backup_dir} does not exist."

    actual_files = sorted(os.listdir(clean_backup_dir))
    assert actual_files == expected_files, f"Files in {clean_backup_dir} do not match expected. Actual: {actual_files}, Expected: {expected_files}"

def test_archive_creation(expected_files):
    archive_path = "/home/user/elf_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        tar_members = tar.getnames()

    # Check that tar members are exactly the expected files (no directory paths)
    sorted_members = sorted(tar_members)
    assert sorted_members == expected_files, f"Archive contents do not match expected. Actual: {sorted_members}, Expected: {expected_files}"

def test_archive_contents_log(expected_files):
    log_path = "/home/user/archive_contents.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_files, f"Contents of {log_path} do not match expected sorted filenames. Actual: {content}, Expected: {expected_files}"