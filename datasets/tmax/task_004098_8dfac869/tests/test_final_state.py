# test_final_state.py

import os
import stat
import pytest

def test_config_symlink():
    symlink_path = "/home/user/config"
    target_path = "/home/user/capacity-config"

    assert os.path.islink(symlink_path), f"'{symlink_path}' is not a symbolic link."

    actual_target = os.readlink(symlink_path)
    # The user might have used a relative path or absolute path for the symlink target.
    # We should resolve it to absolute to be robust, but the task specifically says:
    # "Create a symbolic link so the C program can find its configuration"
    # Actually, as long as it resolves to the correct directory, it's fine.
    resolved_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), actual_target))
    assert resolved_target == target_path, f"Symlink '{symlink_path}' points to '{actual_target}', expected it to resolve to '{target_path}'."

def test_planner_executable():
    planner_bin = "/home/user/planner"
    assert os.path.isfile(planner_bin), f"Compiled binary '{planner_bin}' is missing."

    st = os.stat(planner_bin)
    assert bool(st.st_mode & stat.S_IXUSR), f"'{planner_bin}' is not executable."

def test_start_services_script():
    script_path = "/home/user/start_services.sh"
    assert os.path.isfile(script_path), f"Script '{script_path}' is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"'{script_path}' is not executable."

def test_planner_output_log():
    log_path = "/home/user/planner_output.log"
    assert os.path.isfile(log_path), f"Log file '{log_path}' is missing. Did you run the start_services.sh script?"

    with open(log_path, "r") as f:
        content = f.read()

    expected_content = "Connection successful. Configuration loaded: CAPACITY_LIMIT=8500\n"
    assert content == expected_content, f"Log file '{log_path}' content does not match expected output.\nExpected: {repr(expected_content)}\nGot: {repr(content)}"