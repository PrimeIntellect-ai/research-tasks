# test_final_state.py

import os
import subprocess
import pytest

def test_directories_exist():
    """Test that all required directories have been created."""
    dirs = [
        "/home/user/src",
        "/home/user/bin",
        "/home/user/logs",
        "/home/user/scripts",
        "/home/user/config",
        "/home/user/.config/systemd/user"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_c_source_code():
    """Test that the C source code exists and contains required elements."""
    src_file = "/home/user/src/microservice.c"
    assert os.path.isfile(src_file), f"Source file {src_file} does not exist."

    with open(src_file, "r") as f:
        content = f.read()

    required_strings = [
        "SERVICE_OK\\n",
        "/home/user/logs/micro.log",
        "fopen",
        "fprintf",
        "fflush",
        "sleep"
    ]
    for req in required_strings:
        assert req in content, f"Expected '{req}' to be in {src_file}"

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    bin_file = "/home/user/bin/microservice"
    assert os.path.isfile(bin_file), f"Executable {bin_file} does not exist."
    assert os.access(bin_file, os.X_OK), f"File {bin_file} is not executable."

def test_systemd_service_file():
    """Test that the systemd service file exists and has correct contents."""
    service_file = "/home/user/.config/systemd/user/micro.service"
    assert os.path.isfile(service_file), f"Service file {service_file} does not exist."

    with open(service_file, "r") as f:
        content = f.read()

    assert "Description=Microservice Daemon" in content, "Missing correct Description in service file."
    assert "ExecStart=/home/user/bin/microservice" in content, "Missing correct ExecStart in service file."
    assert "Restart=always" in content, "Missing Restart=always in service file."

def test_logrotate_script_and_config():
    """Test the logrotate script's existence, execution, idempotency, and the resulting config."""
    script_file = "/home/user/scripts/setup_logrotate.sh"
    config_file = "/home/user/config/micro-logrotate.conf"

    assert os.path.isfile(script_file), f"Script {script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"Script {script_file} is not executable."

    # Run the script twice to test idempotency
    subprocess.run([script_file], check=True)
    subprocess.run([script_file], check=True)

    assert os.path.isfile(config_file), f"Config file {config_file} was not created."

    with open(config_file, "r") as f:
        lines = f.readlines()

    assert len(lines) < 25, "Config file is too long, script might not be idempotent."

    content = "".join(lines)
    assert "/home/user/logs/micro.log" in content, "Config does not target /home/user/logs/micro.log"
    assert "hourly" in content, "Config missing 'hourly'"
    assert "rotate 5" in content, "Config missing 'rotate 5'"
    assert "missingok" in content, "Config missing 'missingok'"
    assert "compress" in content, "Config missing 'compress'"
    assert "copytruncate" in content, "Config missing 'copytruncate'"