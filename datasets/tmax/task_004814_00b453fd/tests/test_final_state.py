# test_final_state.py

import os
import re
import subprocess

def test_directories_and_symlink():
    """Check directory structure and symlink."""
    archive_dir = "/home/user/capacity/logs/archive"
    symlink_path = "/home/user/capacity/active_logs"
    target_dir = "/home/user/capacity/logs"

    assert os.path.isdir(archive_dir), f"Directory {archive_dir} does not exist."
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    # Check symlink target
    target = os.readlink(symlink_path)
    assert target == target_dir, f"Symlink {symlink_path} points to {target}, expected {target_dir}."

def test_c_program_exists_and_executable():
    """Check that tracker.c exists and tracker is compiled and executable."""
    c_file = "/home/user/capacity/tracker.c"
    executable = "/home/user/capacity/tracker"

    assert os.path.isfile(c_file), f"Source file {c_file} does not exist."
    assert os.path.isfile(executable), f"Executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_log_output_and_format():
    """Check the log file exists and has the correct format with HST timezone."""
    log_file = "/home/user/capacity/logs/resource.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist. Did you run the tracker?"

    with open(log_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 1, f"Log file {log_file} is empty."

    last_line = lines[-1]
    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} HST\] LOAD: \d+\.\d+$"
    assert re.match(pattern, last_line), f"Log line '{last_line}' does not match expected format."

def test_rotate_script_and_execution():
    """Check that rotate.sh exists, is executable, and works correctly."""
    script_path = "/home/user/capacity/rotate.sh"
    log_file = "/home/user/capacity/logs/resource.log"
    rotated_file = "/home/user/capacity/logs/archive/resource_rotated.log"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed to execute properly."

    # Verify the move
    assert not os.path.isfile(log_file), f"Log file {log_file} still exists after running rotate.sh."
    assert os.path.isfile(rotated_file), f"Rotated log file {rotated_file} does not exist after running rotate.sh."