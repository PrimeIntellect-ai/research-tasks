# test_final_state.py

import os
import json
import subprocess
import pytest

def test_directories_and_symlinks():
    real_conf = "/home/user/real_conf"
    real_logs = "/home/user/real_logs"
    sym_conf = "/home/user/service/conf"
    sym_logs = "/home/user/service/logs"

    assert os.path.isdir(real_conf), f"{real_conf} is missing or not a directory"
    assert os.path.isdir(real_logs), f"{real_logs} is missing or not a directory"

    assert os.path.islink(sym_conf), f"{sym_conf} is not a symlink"
    assert os.readlink(sym_conf) == real_conf, f"{sym_conf} does not point to {real_conf}"

    assert os.path.islink(sym_logs), f"{sym_logs} is not a symlink"
    assert os.readlink(sym_logs) == real_logs, f"{sym_logs} does not point to {real_logs}"

def test_expect_script_exists():
    expect_script = "/home/user/setup_netmon.exp"
    assert os.path.isfile(expect_script), f"{expect_script} is missing"

def test_settings_json():
    settings_path = "/home/user/service/conf/settings.json"
    assert os.path.isfile(settings_path), f"{settings_path} is missing"

    with open(settings_path, "r") as f:
        try:
            settings = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{settings_path} is not valid JSON")

    assert settings.get("configured") is True, "settings.json does not have 'configured': true"
    assert settings.get("user") == "sysadmin", "settings.json does not have correct user"
    assert settings.get("group") == "netops", "settings.json does not have correct group"

def test_supervisord_conf():
    conf_path = "/home/user/supervisor/supervisord.conf"
    assert os.path.isfile(conf_path), f"{conf_path} is missing"

    with open(conf_path, "r") as f:
        content = f.read()

    # Check if the command is correctly set
    # It could be 'command=python3 /home/user/service/netmon.py --serve'
    assert "command=python3 /home/user/service/netmon.py --serve" in content or \
           "command = python3 /home/user/service/netmon.py --serve" in content, \
           "supervisord.conf does not contain the correct command for netmon"

def test_processes_running():
    # Check if supervisord is running
    cmd_supervisord = ["pgrep", "-f", "supervisord"]
    proc_supervisord = subprocess.run(cmd_supervisord, stdout=subprocess.PIPE)
    assert proc_supervisord.returncode == 0, "supervisord is not running"

    # Check if netmon.py --serve is running
    cmd_netmon = ["pgrep", "-f", "netmon.py --serve"]
    proc_netmon = subprocess.run(cmd_netmon, stdout=subprocess.PIPE)
    assert proc_netmon.returncode == 0, "netmon.py --serve is not running"

def test_logs_and_success_file():
    log_path = "/home/user/service/logs/status.log"
    success_path = "/home/user/success.txt"

    assert os.path.isfile(log_path), f"{log_path} is missing"
    with open(log_path, "r") as f:
        log_content = f.read().strip()
    assert "SERVICE_ONLINE" in log_content, f"{log_path} does not contain 'SERVICE_ONLINE'"

    assert os.path.isfile(success_path), f"{success_path} is missing"
    with open(success_path, "r") as f:
        success_content = f.read().strip()
    assert success_content == "SERVICE_ONLINE", f"{success_path} does not contain exactly 'SERVICE_ONLINE'"