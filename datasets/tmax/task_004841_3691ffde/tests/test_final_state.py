# test_final_state.py

import os
import stat
import re

def test_status_log_contents():
    log_path = "/home/user/proxy/status.log"
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "200 OK: Upstream connected"
    assert content == expected_content, f"Expected '{expected_content}' in {log_path}, got '{content}'"

def test_symlink_created_correctly():
    symlink_path = "/home/user/proxy/run/upstream.sock"
    expected_target = "/home/user/_service/tmp/backend.sock"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    actual_target = os.readlink(symlink_path)
    assert actual_target == expected_target, f"Symlink points to {actual_target}, expected {expected_target}"

def test_bash_profile_updated():
    profile_path = "/home/user/.bash_profile"
    assert os.path.exists(profile_path), f"{profile_path} does not exist."

    with open(profile_path, "r") as f:
        content = f.read()

    assert 'SOCKET_MAPPING_DIR="/home/user/proxy/run"' in content, \
        f"SOCKET_MAPPING_DIR assignment missing in {profile_path}."

    assert '/home/user/bin' in content and 'PATH' in content, \
        f"PATH update for /home/user/bin missing in {profile_path}."

def test_start_stack_script_requirements():
    script_path = "/home/user/bin/start_stack.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert re.search(r'\bdf\b', content), f"'df' command missing in {script_path}."
    assert re.search(r'\b(grep|awk|sed)\b', content), f"Text processing tool (grep, awk, or sed) missing in {script_path}."
    assert "daemon.c" in content, f"'daemon.c' reference missing in {script_path}."
    assert "ln -s" in content or "ln -sf" in content, f"'ln -s' command missing in {script_path}."

def test_daemon_compiled():
    daemon_path = "/home/user/bin/daemon"
    assert os.path.exists(daemon_path), f"Compiled daemon {daemon_path} does not exist."

    st = os.stat(daemon_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{daemon_path} is not executable."

def test_directories_exist():
    dirs = [
        "/home/user/bin",
        "/home/user/proxy/run",
        "/home/user/_service/tmp"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} was not created."