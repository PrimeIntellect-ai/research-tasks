# test_final_state.py

import os
import re
import pytest

def test_legacy_daemon_compiled():
    """Test that the C source was compiled to the expected executable."""
    executable = "/home/user/legacy_daemon"
    assert os.path.isfile(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_expect_script_exists():
    """Test that the expect script was created."""
    script_file = "/home/user/trigger_migration.exp"
    assert os.path.isfile(script_file), f"Expect script {script_file} is missing."

    with open(script_file, "r") as f:
        content = f.read()

    # Check for some basic expect commands and strings
    assert "spawn" in content, f"Expect script {script_file} does not contain 'spawn'."
    assert "cloud_admin_99" in content, f"Expect script {script_file} does not contain 'cloud_admin_99'."
    assert "START_MIGRATE" in content, f"Expect script {script_file} does not contain 'START_MIGRATE'."
    assert "10.0.0.50" in content, f"Expect script {script_file} does not contain '10.0.0.50'."

def test_migration_run_log():
    """Test that the expect script was run and output redirected to the log file."""
    log_file = "/home/user/migration_run.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    with open(log_file, "r") as f:
        content = f.read()

    expected_success = "SUCCESS: Migration started to 10.0.0.50"
    assert expected_success in content, f"Log file {log_file} does not contain the expected success message: '{expected_success}'."

def test_migration_cron_file():
    """Test that the cron file was created with the correct schedule and command."""
    cron_file = "/home/user/migration.cron"
    assert os.path.isfile(cron_file), f"Cron file {cron_file} is missing."

    with open(cron_file, "r") as f:
        lines = f.readlines()

    valid_cron_found = False
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Expecting: 0 * * * * /usr/bin/expect /home/user/trigger_migration.exp > /home/user/migration_run.log
        # Allow multiple spaces
        if re.match(r'^0\s+\*\s+\*\s+\*\s+\*\s+/usr/bin/expect\s+/home/user/trigger_migration\.exp\s*>\s*/home/user/migration_run\.log$', line):
            valid_cron_found = True
            break

    assert valid_cron_found, f"Cron file {cron_file} does not contain the correct cron schedule and command."