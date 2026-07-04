# test_final_state.py
import os
import stat
import urllib.request
import urllib.error
import re
import configparser

def test_deploy_log_and_process():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Deployment log {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in deploy.log, found {len(lines)}."
    assert lines[0] == "[SUCCESS] Extracted files", "Line 1 of deploy.log is incorrect."
    assert lines[1] == "[SUCCESS] Permissions hardened", "Line 2 of deploy.log is incorrect."
    assert lines[2] == "[SUCCESS] Config updated", "Line 3 of deploy.log is incorrect."

    match = re.match(r"\[SUCCESS\] Service running on PID (\d+)", lines[3])
    assert match, "Line 4 of deploy.log does not match expected format."

    pid = int(match.group(1))

    # Check if process is running
    cmdline_path = f"/proc/{pid}/cmdline"
    assert os.path.exists(cmdline_path), f"Process with PID {pid} is not running."

    with open(cmdline_path, "r") as f:
        cmdline = f.read().replace('\x00', ' ')

    assert "server.py" in cmdline, f"Process {pid} does not appear to be server.py. Cmdline: {cmdline}"

def test_server_running_on_port_9090():
    url = "http://127.0.0.1:9090/"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode('utf-8')
            assert body == "OK", f"Expected response 'OK', got '{body}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to server on port 9090: {e}"

def test_permissions():
    bin_dir = "/home/user/app/bin"
    config_dir = "/home/user/app/config"

    assert os.path.isdir(bin_dir), f"{bin_dir} does not exist."
    assert os.path.isdir(config_dir), f"{config_dir} does not exist."

    for filename in os.listdir(bin_dir):
        filepath = os.path.join(bin_dir, filename)
        if os.path.isfile(filepath):
            mode = stat.S_IMODE(os.stat(filepath).st_mode)
            assert mode == 0o500, f"File {filepath} has permissions {oct(mode)}, expected 0o500."

    for filename in os.listdir(config_dir):
        filepath = os.path.join(config_dir, filename)
        if os.path.isfile(filepath):
            mode = stat.S_IMODE(os.stat(filepath).st_mode)
            assert mode == 0o400, f"File {filepath} has permissions {oct(mode)}, expected 0o400."

def test_config_updated():
    config_path = "/home/user/app/config/worker.ini"
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

    # Temporarily change permission to read it if it's 0400 but owned by another user (though we are root/user)
    # Since we are running tests, we should be able to read 0400 if we are the owner, or root.
    try:
        config = configparser.ConfigParser()
        config.read(config_path)
    except Exception as e:
        assert False, f"Failed to parse {config_path}: {e}"

    assert "Unit" in config, "Missing [Unit] section in worker.ini"
    assert "Service" in config, "Missing [Service] section in worker.ini"

    # configparser might not preserve the exact key case or might fail if After=network.target is added without a key.
    # Actually After=network.target is a valid key-value pair.
    assert config.get("Unit", "After", fallback="") == "network.target", "After=network.target missing or incorrect in [Unit] section."
    assert config.get("Service", "Port", fallback="") == "9090", "Port=9090 missing or incorrect in [Service] section."