# test_final_state.py

import os
import stat
import subprocess
import tempfile

def test_start_forwarding_sh():
    script_path = "/home/user/start_forwarding.sh"
    assert os.path.exists(script_path), f"File {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "socat" in content, "The script does not contain a socat command."
    assert "8333" in content, "The script does not contain the port 8333."
    assert "9333" in content, "The script does not contain the port 9333."
    assert "127.0.0.1" in content, "The script does not bind/connect to 127.0.0.1."
    assert "/home/user/raw_traffic.log" in content, "The script does not log to /home/user/raw_traffic.log."

def test_alert_py():
    script_path = "/home/user/alert.py"
    assert os.path.exists(script_path), f"File {script_path} does not exist."

    dummy_log = "/home/user/dummy_traffic.log"
    blocked_log = "/home/user/blocked.log"

    # Clean up blocked_log if it exists from previous tests
    if os.path.exists(blocked_log):
        os.remove(blocked_log)

    with open(dummy_log, "w") as f:
        f.write("Normal traffic data\n")
        f.write("BLOCKED_IP from 192.168.1.1\n")
        f.write("More traffic\n")
        f.write("Another BLOCKED_IP recorded\n")

    try:
        subprocess.run(["python3", script_path, dummy_log], check=True)

        assert os.path.exists(blocked_log), f"The script did not create {blocked_log}."

        with open(blocked_log, "r") as f:
            lines = f.read().splitlines()

        assert len(lines) == 2, f"Expected 2 lines in {blocked_log}, but got {len(lines)}."
        assert lines[0] == "ALERT: A blocked connection was detected.", "Incorrect alert message."
        assert lines[1] == "ALERT: A blocked connection was detected.", "Incorrect alert message."
    finally:
        if os.path.exists(dummy_log):
            os.remove(dummy_log)
        if os.path.exists(blocked_log):
            os.remove(blocked_log)

def test_alert_rotate_conf():
    conf_path = "/home/user/alert_rotate.conf"
    assert os.path.exists(conf_path), f"File {conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/blocked.log" in content, "The logrotate config does not target /home/user/blocked.log."

    keywords = ["daily", "rotate 5", "compress", "missingok", "notifempty"]
    for kw in keywords:
        # allow multiple spaces between rotate and 5
        if kw == "rotate 5":
            assert "rotate" in content and "5" in content, "The logrotate config does not specify 'rotate 5'."
        else:
            assert kw in content, f"The logrotate config does not contain the directive '{kw}'."