# test_final_state.py
import os
import re

def test_supervisor_script_exists():
    path = "/home/user/supervisor.py"
    assert os.path.isfile(path), f"Supervisor script missing at {path}"

def test_summary_file_exists_and_content():
    path = "/home/user/summary.txt"
    assert os.path.isfile(path), f"Summary file missing at {path}"

    with open(path, "r") as f:
        content = f.read()

    restarts_match = re.search(r"Restarts:\s*(\d+)", content)
    backups_match = re.search(r"Backups:\s*(\d+)", content)
    backup_dir_match = re.search(r"Backup_Dir:\s*(\S+)", content)

    assert restarts_match, "Could not find 'Restarts: <number>' in summary.txt"
    assert backups_match, "Could not find 'Backups: <number>' in summary.txt"
    assert backup_dir_match, "Could not find 'Backup_Dir: <path>' in summary.txt"

    restarts = int(restarts_match.group(1))
    backups = int(backups_match.group(1))
    backup_dir = backup_dir_match.group(1)

    assert restarts > 0, f"Expected Restarts > 0, got {restarts}"
    assert backups > 0, f"Expected Backups > 0, got {backups}"
    assert backup_dir == "/home/user/secure_backups", f"Expected Backup_Dir to be '/home/user/secure_backups', got {backup_dir}"

def test_backup_directory_and_files():
    backup_dir = "/home/user/secure_backups"
    assert os.path.isdir(backup_dir), f"Backup directory missing at {backup_dir}"

    files = os.listdir(backup_dir)
    backup_files = [f for f in files if f.startswith("backup_") and f.endswith(".log")]

    assert len(backup_files) > 0, f"No backup files found in {backup_dir}"

    # Check if the number of backups roughly matches the summary file
    summary_path = "/home/user/summary.txt"
    if os.path.isfile(summary_path):
        with open(summary_path, "r") as f:
            content = f.read()
            backups_match = re.search(r"Backups:\s*(\d+)", content)
            if backups_match:
                reported_backups = int(backups_match.group(1))
                assert len(backup_files) == reported_backups, f"Reported backups ({reported_backups}) does not match actual backup files count ({len(backup_files)})"

def test_logs_directory_and_files():
    logs_dir = "/home/user/logs"
    assert os.path.isdir(logs_dir), f"Logs directory missing at {logs_dir}"

    flappy_log = os.path.join(logs_dir, "flappy.log")
    assert os.path.isfile(flappy_log), f"Main log file missing at {flappy_log}"

    # Check if there are rotated logs
    files = os.listdir(logs_dir)
    rotated_logs = [f for f in files if re.match(r"flappy\.log\.[1-3]", f)]
    assert len(rotated_logs) > 0, "No rotated log files found (e.g., flappy.log.1) in /home/user/logs"