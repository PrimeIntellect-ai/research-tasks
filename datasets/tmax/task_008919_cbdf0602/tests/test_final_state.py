# test_final_state.py

import os

def test_backup_dir_contents():
    """Verify that the backup directory contains exactly the expected .txt files."""
    backup_dir = "/home/user/backup_dir"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist."

    expected_files = {
        "another file.txt",
        "file 1.txt",
        "file2.txt",
        "normal.txt"
    }

    actual_files = set(os.listdir(backup_dir))

    missing_files = expected_files - actual_files
    assert not missing_files, f"Missing files in backup directory: {missing_files}"

    unexpected_files = actual_files - expected_files
    assert not unexpected_files, f"Unexpected files in backup directory: {unexpected_files}"

def test_success_log_contents():
    """Verify that success.log contains the sorted list of backed-up .txt files."""
    log_file = "/home/user/success.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read().strip().splitlines()

    expected_content = [
        "another file.txt",
        "file 1.txt",
        "file2.txt",
        "normal.txt"
    ]

    assert content == expected_content, f"Contents of {log_file} do not match the expected sorted list of filenames. Got: {content}"

def test_backup_script_executable():
    """Verify that the backup script is still executable."""
    script_path = "/home/user/backup.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is no longer executable."