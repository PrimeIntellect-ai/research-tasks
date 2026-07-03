# test_final_state.py

import os
import stat

def test_directories_exist():
    """Verify that the required directories have been created."""
    dirs = [
        "/home/user/capacity_planner/src",
        "/home/user/capacity_planner/bin",
        "/home/user/capacity_planner/logs",
        "/home/user/capacity_planner/active"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} is missing."

def test_cpp_source_and_binary():
    """Verify that the C++ source file and compiled binary exist."""
    src_file = "/home/user/capacity_planner/src/monitor_mock.cpp"
    bin_file = "/home/user/capacity_planner/bin/monitor"

    assert os.path.isfile(src_file), f"C++ source file {src_file} is missing."
    assert os.path.isfile(bin_file), f"Compiled binary {bin_file} is missing."
    assert os.access(bin_file, os.X_OK), f"Compiled binary {bin_file} is not executable."

def test_symlink():
    """Verify that the symlink exists and points to the correct binary."""
    symlink_path = "/home/user/capacity_planner/active/current_monitor"
    target_path = "/home/user/capacity_planner/bin/monitor"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.readlink(symlink_path) == target_path, f"Symlink {symlink_path} does not point to {target_path}."

def test_health_check_script():
    """Verify that the health check script exists and is executable."""
    script_path = "/home/user/capacity_planner/health_check.sh"

    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_log_file_content():
    """Verify that the log file was generated and contains the correct alerts."""
    log_path = "/home/user/capacity_planner/logs/critical_alerts.log"

    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_alerts = ["backend_api", "database_main", "ml_worker"]

    assert content == expected_alerts, f"Log file content does not match expected alerts. Got {content}, expected {expected_alerts}."