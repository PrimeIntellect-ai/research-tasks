# test_final_state.py

import os
import stat
import pytest

def test_update_config_script_exists():
    script_path = "/home/user/update_config.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_proxy_conf_updated():
    proxy_conf_path = "/home/user/deploy/proxy.conf"
    server_conf_path = "/home/user/app/server.conf"

    assert os.path.isfile(server_conf_path), f"{server_conf_path} does not exist."
    assert os.path.isfile(proxy_conf_path), f"{proxy_conf_path} does not exist."

    bind_path = None
    with open(server_conf_path, "r") as f:
        for line in f:
            if line.startswith("BIND_PATH="):
                bind_path = line.strip().split("=", 1)[1]
                break

    assert bind_path is not None, "BIND_PATH not found in server.conf"

    with open(proxy_conf_path, "r") as f:
        proxy_content = f.read()

    expected_directive = f"proxy_pass http://unix:{bind_path};"
    assert expected_directive in proxy_content, f"Expected '{expected_directive}' in {proxy_conf_path}, but it was not found."

def test_hcheck_executable_exists():
    hcheck_path = "/home/user/hcheck"
    assert os.path.isfile(hcheck_path), f"Executable {hcheck_path} does not exist."

    # Check if it's executable
    st = os.stat(hcheck_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"{hcheck_path} is not executable."

    # Check if it's an ELF file
    with open(hcheck_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{hcheck_path} is not a valid ELF executable."

def test_health_report_log():
    log_path = "/home/user/health_report.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "HEALTHY", f"Expected 'HEALTHY' in {log_path}, got '{content}'."