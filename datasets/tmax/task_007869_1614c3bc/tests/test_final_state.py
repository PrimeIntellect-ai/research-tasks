# test_final_state.py
import os
import re
import stat

def test_directories_and_permissions():
    """Check that required directories exist and have correct permissions."""
    bin_dir = "/home/user/deploy/bin"
    logs_dir = "/home/user/deploy/logs"

    assert os.path.isdir(bin_dir), f"Directory {bin_dir} does not exist."
    assert os.path.isdir(logs_dir), f"Directory {logs_dir} does not exist."

    # Check permissions of bin_dir (must be 700)
    mode = os.stat(bin_dir).st_mode
    assert stat.S_IMODE(mode) == 0o700, f"Permissions for {bin_dir} are not 700."

def test_source_file_exists():
    """Check that the C source file exists."""
    src_file = "/home/user/monitor_src/resource_monitor.c"
    assert os.path.isfile(src_file), f"Source file {src_file} does not exist."

def test_symlink_verification():
    """Check that the symlink is correctly set up."""
    symlink_path = "/home/user/deploy/current_log"
    target_path = "/home/user/deploy/logs/active.csv"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    # Check the target of the symlink
    target = os.readlink(symlink_path)
    assert target == target_path, f"Symlink target is '{target}', expected '{target_path}'."

def test_executable_exists():
    """Check that the compiled monitor executable exists and is executable."""
    exe_path = "/home/user/deploy/bin/monitor"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"Executable {exe_path} is not executable."

def test_log_file_content():
    """Check that the log file exists and contains properly formatted data."""
    log_file = "/home/user/deploy/logs/active.csv"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 1, f"Log file {log_file} is empty."

    # Regex pattern: <unix_timestamp>,<load_1_min>,<mem_used_kb>,<mem_total_kb>
    pattern = re.compile(r"^[0-9]+,[0-9]+\.[0-9]+,[0-9]+,[0-9]+$")

    match_found = any(pattern.match(line.strip()) for line in lines)
    assert match_found, f"No lines in {log_file} match the expected CSV format."