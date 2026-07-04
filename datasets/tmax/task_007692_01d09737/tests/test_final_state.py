# test_final_state.py

import os
import re
import stat

def test_nginx_upstream_conf_content():
    discovery_log = "/home/user/app/discovery.log"
    assert os.path.isfile(discovery_log), f"{discovery_log} is missing."

    with open(discovery_log, "r") as f:
        content = f.read()

    match = re.search(r"BIND_ADDR=(\S+)", content)
    assert match is not None, "Could not find BIND_ADDR in discovery.log"
    socket_path = match.group(1)

    conf_file = "/home/user/app/nginx-upstream.conf"
    assert os.path.isfile(conf_file), f"{conf_file} was not generated."

    with open(conf_file, "r") as f:
        conf_content = f.read().strip()

    expected_conf = f"upstream backend {{ server unix:{socket_path}; }}"
    assert conf_content == expected_conf, f"Expected '{expected_conf}', but got '{conf_content}' in {conf_file}"

def test_daemon_log_rotated_old_content():
    old_log = "/home/user/app/daemon.log.1"
    assert os.path.isfile(old_log), f"{old_log} is missing. Did the rotation script run?"

    with open(old_log, "r") as f:
        content = f.read()

    assert "ERROR: Connection refused to" in content, f"{old_log} does not contain the expected old log content."

def test_daemon_log_new_content():
    new_log = "/home/user/app/daemon.log"
    assert os.path.isfile(new_log), f"{new_log} is missing."

    with open(new_log, "r") as f:
        content = f.read()

    assert content == "--- LOG ROTATED ---\n", f"Expected exactly '--- LOG ROTATED ---' (with newline) in {new_log}, got {repr(content)}"

def test_rotate_script_exists_and_executable():
    script_file = "/home/user/app/rotate.sh"
    assert os.path.isfile(script_file), f"{script_file} is missing."

    st = os.stat(script_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_file} is not executable."