# test_final_state.py

import os

def test_script_exists_and_executable():
    script_path = "/home/user/audit_backups.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_quarantine_directory_exists():
    quarantine_dir = "/home/user/quarantine"
    assert os.path.isdir(quarantine_dir), f"Quarantine directory {quarantine_dir} does not exist."

def test_quarantine_symlinks():
    expected_symlinks = {
        "/home/user/quarantine/system.tar.gz": "/home/user/backups/server_alpha/system.tar.gz",
        "/home/user/quarantine/data.tar.gz": "/home/user/backups/server_beta/archive/data.tar.gz",
    }

    for symlink_path, target_path in expected_symlinks.items():
        assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
        actual_target = os.readlink(symlink_path)
        assert actual_target == target_path, f"Symlink {symlink_path} points to {actual_target}, expected {target_path}."

def test_quarantine_log():
    log_path = "/home/user/quarantine_log.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        log_content = f.read().splitlines()

    expected_lines = [
        "VULNERABLE: /home/user/backups/server_alpha/system.tar.gz -> var/log/../../../etc/shadow",
        "VULNERABLE: /home/user/backups/server_beta/archive/data.tar.gz -> ../.ssh/authorized_keys"
    ]

    for expected_line in expected_lines:
        assert expected_line in log_content, f"Expected log entry not found: {expected_line}"

    # Check that there are no extra vulnerable lines
    vulnerable_lines = [line for line in log_content if line.startswith("VULNERABLE:")]
    assert len(vulnerable_lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} VULNERABLE lines, found {len(vulnerable_lines)}."