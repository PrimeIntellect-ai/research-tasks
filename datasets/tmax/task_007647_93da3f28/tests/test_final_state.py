# test_final_state.py

import os
import subprocess
import pytest

def test_monitor_log_contents():
    log_path = '/home/user/monitor_log.txt'
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "alice:ACTIVE",
        "bob:INACTIVE",
        "charlie:INACTIVE"
    ]

    assert sorted(lines) == expected_lines, f"Log contents mismatch. Expected {expected_lines}, got {sorted(lines)}"

def test_active_links_directory():
    links_dir = '/home/user/active_links'
    assert os.path.isdir(links_dir), f"Directory {links_dir} does not exist."

    active_links = os.listdir(links_dir)
    assert "alice" in active_links, "Symlink 'alice' is missing from active_links directory."
    assert len(active_links) == 1, f"active_links directory should only contain 'alice', found: {active_links}"

    link_path = os.path.join(links_dir, 'alice')
    assert os.path.islink(link_path), f"{link_path} is not a symbolic link."

    link_target = os.readlink(link_path)
    expected_target = '/home/user/managed_users/alice'
    assert link_target == expected_target, f"Symlink target mismatch. Expected {expected_target}, got {link_target}"

def test_schedule_monitor_running():
    script_path = '/home/user/schedule_monitor.sh'
    assert os.path.exists(script_path), f"Scheduling script {script_path} does not exist."

    try:
        output = subprocess.check_output(["pgrep", "-f", "schedule_monitor.sh"], text=True)
        assert output.strip(), "schedule_monitor.sh is not running in the background."
    except subprocess.CalledProcessError:
        pytest.fail("schedule_monitor.sh is not running in the background.")

def test_cpp_program_exists():
    cpp_source = '/home/user/account_monitor.cpp'
    cpp_executable = '/home/user/account_monitor'

    assert os.path.isfile(cpp_source), f"C++ source file {cpp_source} does not exist."
    assert os.path.isfile(cpp_executable), f"Compiled executable {cpp_executable} does not exist."
    assert os.access(cpp_executable, os.X_OK), f"File {cpp_executable} is not executable."