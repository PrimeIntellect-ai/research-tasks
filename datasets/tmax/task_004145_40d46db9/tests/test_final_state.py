# test_final_state.py

import os
import time
import subprocess
import re
import uuid
import pytest

def test_directory_setup_and_acls():
    """Verify /home/user/secure_zone exists and has default mask r-x."""
    dir_path = "/home/user/secure_zone"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    result = subprocess.run(["getfacl", dir_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run getfacl."
    assert "default:mask::r-x" in result.stdout, f"Default mask is not r-x for {dir_path}."

def test_c_program_presence_and_execution():
    """Verify fs_monitor exists, is executable, and logs new files."""
    prog_path = "/home/user/fs_monitor"
    log_path = "/home/user/events.log"
    dir_path = "/home/user/secure_zone"

    assert os.path.isfile(prog_path), f"Compiled program {prog_path} does not exist."
    assert os.access(prog_path, os.X_OK), f"Program {prog_path} is not executable."

    # Create a unique file to test the running monitor
    unique_filename = f"test_alert_{uuid.uuid4().hex}.txt"
    test_file_path = os.path.join(dir_path, unique_filename)

    try:
        with open(test_file_path, "w") as f:
            f.write("test")

        # Give the monitor some time to process and write to the log
        time.sleep(1.5)

        assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Is the monitor running?"

        with open(log_path, "r") as f:
            log_content = f.read()

        expected_log = f"ALERT: New file {unique_filename} detected"
        assert expected_log in log_content, f"Expected log '{expected_log}' not found in {log_path}."

    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_log_parsing_pipeline():
    """Verify process_alerts.sh extracts filenames correctly."""
    script_path = "/home/user/process_alerts.sh"
    output_path = "/home/user/processed_files.txt"
    log_path = "/home/user/events.log"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed to execute."

    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    # We check if the last file we created in the previous test is in the processed files
    # Let's just create a dummy log entry to be absolutely sure
    dummy_file = f"dummy_{uuid.uuid4().hex}.txt"
    with open(log_path, "a") as f:
        f.write(f"ALERT: New file {dummy_file} detected\n")

    subprocess.run([script_path], capture_output=True, text=True)

    with open(output_path, "r") as f:
        processed_content = f.read()

    assert dummy_file in processed_content, f"Filename {dummy_file} was not extracted to {output_path}."

def test_ssh_tunnel_configuration():
    """Verify start_tunnel.sh contains the correct SSH command."""
    script_path = "/home/user/start_tunnel.sh"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert re.search(r"ssh\s+", content), "No ssh command found in the script."
    assert re.search(r"-L\s+8888:127\.0\.0\.1:9999", content), "Port forwarding (-L 8888:127.0.0.1:9999) not correctly configured."
    assert "-N" in content.split(), "Missing -N flag for no command execution."
    assert "-f" in content.split(), "Missing -f flag to run in background."
    assert "monitor-server" in content, "Missing monitor-server alias in the ssh command."