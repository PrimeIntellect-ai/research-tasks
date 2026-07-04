# test_final_state.py

import os
import re
import configparser

def test_health_log_exists_and_contains_status_ok():
    log_path = "/home/user/logs/health.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run the script manually and create the directory?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "STATUS: OK" in content, f"Log file {log_path} does not contain the expected string 'STATUS: OK'."

def test_systemd_service_file():
    service_path = "/home/user/.config/systemd/user/health-check.service"
    assert os.path.isfile(service_path), f"Service file {service_path} does not exist."

    config = configparser.ConfigParser(strict=False)
    # systemd files can have no section headers at the very top sometimes, but usually start with [Unit]
    # configparser needs a section header.
    try:
        config.read(service_path)
    except configparser.MissingSectionHeaderError:
        with open(service_path, "r") as f:
            content = "[DEFAULT]\n" + f.read()
        config.read_string(content)

    # Check if ExecStart is correct
    exec_start = None
    if "Service" in config:
        exec_start = config["Service"].get("ExecStart")
    elif "DEFAULT" in config:
        exec_start = config["DEFAULT"].get("ExecStart")

    # Fallback to simple string matching if configparser fails due to systemd specific syntax
    if not exec_start:
        with open(service_path, "r") as f:
            content = f.read()
            assert re.search(r"^ExecStart\s*=\s*/home/user/scripts/health_check\.sh", content, re.MULTILINE), \
                f"Service file {service_path} does not contain the correct ExecStart directive."
    else:
        assert exec_start == "/home/user/scripts/health_check.sh", \
            f"Service file {service_path} has incorrect ExecStart: {exec_start}"

def test_systemd_timer_file():
    timer_path = "/home/user/.config/systemd/user/health-check.timer"
    assert os.path.isfile(timer_path), f"Timer file {timer_path} does not exist."

    with open(timer_path, "r") as f:
        content = f.read()

    # Check for OnCalendar with 5 minute intervals. 
    # Valid formats: *:0/5, *:0/5:00, *:0,5,10,15,20,25,30,35,40,45,50,55, etc.
    # We will use a regex to match the most common ones or check the string.
    assert re.search(r"^OnCalendar\s*=\s*.*(\*:0/5|\*:0,5,10)", content, re.MULTILINE), \
        f"Timer file {timer_path} does not contain a valid OnCalendar directive for every 5 minutes."