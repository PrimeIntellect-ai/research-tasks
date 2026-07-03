# test_final_state.py

import os
import subprocess
import tarfile
import pytest

@pytest.fixture(scope="session", autouse=True)
def compile_and_run_c_program():
    """Compiles and runs the student's C program before running tests."""
    c_file = "/home/user/safe_backup.c"
    exe = "/home/user/safe_backup"

    assert os.path.isfile(c_file), f"Source file {c_file} is missing."

    # Compile the C program
    compile_proc = subprocess.run(["gcc", "-o", exe, c_file], capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Compilation failed:\n{compile_proc.stderr}"

    # Execute the compiled program
    run_proc = subprocess.run([exe], capture_output=True, text=True)
    assert run_proc.returncode == 0, f"Execution failed:\n{run_proc.stderr}"

def test_broken_links_renamed():
    """Verifies that looping symlinks were renamed with .broken suffix and originals are gone."""
    expected_broken = [
        "/home/user/config_tree/appB/loop1.broken",
        "/home/user/config_tree/appB/loop2.broken",
        "/home/user/config_tree/appC/loop_self.broken"
    ]
    expected_missing = [
        "/home/user/config_tree/appB/loop1",
        "/home/user/config_tree/appB/loop2",
        "/home/user/config_tree/appC/loop_self"
    ]

    for path in expected_broken:
        assert os.path.islink(path), f"Expected renamed symlink {path} is missing."

    for path in expected_missing:
        assert not os.path.exists(path) and not os.path.islink(path), f"Original looping symlink {path} should have been renamed."

def test_valid_symlinks_untouched():
    """Verifies that valid symlinks and normal files were not modified."""
    valid_link = "/home/user/config_tree/appA/config_link.ini"
    assert os.path.islink(valid_link), f"Valid symlink {valid_link} was incorrectly modified or deleted."
    assert os.readlink(valid_link) == "/home/user/config_tree/appA/config.ini", f"Valid symlink {valid_link} target changed."

def test_broken_links_log():
    """Verifies the contents of the broken_links.log file."""
    log_path = "/home/user/broken_links.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "/home/user/config_tree/appB/loop1",
        "/home/user/config_tree/appB/loop2",
        "/home/user/config_tree/appC/loop_self"
    }

    assert set(lines) == expected_lines, f"Log file contents incorrect. Expected {expected_lines}, got {set(lines)}"
    assert len(lines) == len(expected_lines), "Log file contains duplicate or extra entries."

def test_atomic_archive_creation():
    """Verifies the final archive exists, is valid, and the temporary file is gone."""
    archive_path = "/home/user/config_backup.tar.gz"
    tmp_archive_path = "/home/user/config_backup.tar.gz.tmp"

    assert os.path.isfile(archive_path), f"Final archive {archive_path} is missing."
    assert not os.path.exists(tmp_archive_path), f"Temporary archive {tmp_archive_path} was not cleaned up / renamed."

    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        # Just verifying that the archive contains some of the expected files
        assert any("appB/loop1.broken" in name for name in names), "Archive does not contain the renamed broken links."
        assert any("appA/config.ini" in name for name in names), "Archive does not contain the normal config files."