# test_final_state.py
import os
import time
import json
import subprocess
import pytest

def test_archiver_daemon():
    # 1. Verify filter.sh exists and is executable
    filter_script = "/home/user/filter.sh"
    assert os.path.isfile(filter_script), f"{filter_script} does not exist."
    assert os.access(filter_script, os.X_OK), f"{filter_script} is not executable."

    # 2. Verify archiver executable exists
    archiver_bin = "/home/user/archiver"
    assert os.path.isfile(archiver_bin), f"{archiver_bin} does not exist. Did you compile it?"
    assert os.access(archiver_bin, os.X_OK), f"{archiver_bin} is not executable."

    # 3. Verify the daemon is running
    try:
        ps_output = subprocess.check_output(["ps", "-A", "-o", "comm"]).decode()
        assert "archiver" in ps_output, "The archiver daemon is not running in the background."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check running processes.")

    # 4. Verify initial state (legacy logs processed)
    summary_path = "/home/user/archive/summary.json"
    master_log_path = "/home/user/archive/master_critical.log"

    assert os.path.isfile(summary_path), f"{summary_path} does not exist."
    with open(summary_path, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{summary_path} does not contain valid JSON.")

    assert summary.get("total_critical") == 2, f"Expected total_critical to be 2, got {summary.get('total_critical')}"

    assert os.path.isfile(master_log_path), f"{master_log_path} does not exist."
    with open(master_log_path, "r") as f:
        initial_lines = f.read().splitlines()

    expected_initial_lines = {
        "[CRITICAL] Backup failed on /dev/sda1",
        "[CRITICAL] Connection timeout to backup server"
    }
    assert set(initial_lines) == expected_initial_lines, "master_critical.log does not contain the expected initial critical lines."

    # 5. Trigger incoming file
    incoming_file = "/home/user/incoming/test.log"
    with open(incoming_file, "w") as f:
        f.write("INFO: OK\n[CRITICAL] Incoming failure 1\n[CRITICAL] Incoming failure 2\n")

    # 6. Wait for daemon to process the inotify event
    time.sleep(2)

    # 7. Verify updated state
    with open(summary_path, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{summary_path} does not contain valid JSON after update.")

    assert summary.get("total_critical") == 4, f"Expected total_critical to be 4 after incoming file, got {summary.get('total_critical')}"

    with open(master_log_path, "r") as f:
        final_lines = f.read().splitlines()

    expected_new_lines = {
        "[CRITICAL] Incoming failure 1",
        "[CRITICAL] Incoming failure 2"
    }

    assert len(final_lines) == 4, f"Expected exactly 4 lines in {master_log_path}, got {len(final_lines)}."
    assert expected_initial_lines.union(expected_new_lines) == set(final_lines), "master_critical.log does not contain all expected lines after incoming file processing."