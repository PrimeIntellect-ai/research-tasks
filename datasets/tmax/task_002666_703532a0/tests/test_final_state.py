# test_final_state.py

import os
import subprocess
import pytest

def test_align_logs_executable_exists():
    path = "/home/user/align_logs"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_run_pipeline_script_exists():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

def test_archived_logs_exist():
    archive_a = "/home/user/logs/archive/srv_a.log"
    archive_b = "/home/user/logs/archive/srv_b.log"
    assert os.path.isfile(archive_a), f"Archived log {archive_a} does not exist."
    assert os.path.isfile(archive_b), f"Archived log {archive_b} does not exist."

def test_original_logs_moved():
    orig_a = "/home/user/logs/srv_a.log"
    orig_b = "/home/user/logs/srv_b.log"
    assert not os.path.isfile(orig_a), f"Original log {orig_a} was not moved."
    assert not os.path.isfile(orig_b), f"Original log {orig_b} was not moved."

def test_aligned_csv_content():
    path = "/home/user/output/aligned.csv"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = (
        "timestamp,cpu,mem\n"
        "20,50.00,125.00\n"
        "30,55.00,175.00\n"
        "40,60.25,220.00\n"
        "50,65.00,260.00"
    )

    assert content == expected, f"Content of {path} does not match the expected interpolated values."

def test_crontab_configured():
    try:
        # Run crontab -l for the user 'user'
        result = subprocess.run(
            ["crontab", "-l", "-u", "user"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        crontab_content = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read crontab for 'user': {e.stderr}")

    # Check for the expected cron job
    expected_command = "/home/user/run_pipeline.sh"

    found = False
    for line in crontab_content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            # Check if minute is 15 and command matches
            if parts[0] == "15" and parts[1] == "*" and parts[2] == "*" and parts[3] == "*" and parts[4] == "*":
                if expected_command in line:
                    found = True
                    break

    assert found, "Crontab for 'user' does not contain the correct schedule (15 * * * *) for /home/user/run_pipeline.sh"