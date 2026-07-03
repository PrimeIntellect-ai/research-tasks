# test_final_state.py

import os
import subprocess
import random
import pytest
import re

def test_config_env_fixed():
    config_path = "/home/user/app/config.env"
    assert os.path.isfile(config_path), f"{config_path} is missing"
    with open(config_path, "r") as f:
        content = f.read()

    assert re.search(r"^SHARED_DIR=/home/user/app/shared_logs/?$", content, re.MULTILINE), \
        "config.env does not contain the correct SHARED_DIR path"
    assert re.search(r"^LOG_MODE=binary$", content, re.MULTILINE), \
        "config.env does not contain the correct LOG_MODE=binary"

def test_shared_dir_exists():
    shared_dir = "/home/user/app/shared_logs"
    assert os.path.isdir(shared_dir), f"Shared directory {shared_dir} was not created"

def test_alert_parser_fuzz_equivalence():
    oracle_path = "/home/user/app/oracle_parser"
    agent_path = "/home/user/workspace/alert_parser"

    assert os.path.isfile(oracle_path), f"Oracle parser {oracle_path} missing"
    assert os.path.isfile(agent_path), f"Agent parser {agent_path} missing"
    assert os.access(agent_path, os.X_OK), f"Agent parser {agent_path} is not executable"

    random.seed(42)

    for i in range(1000):
        length = random.randint(0, 1024)
        input_data = bytes(random.getrandbits(8) for _ in range(length))

        try:
            oracle_proc = subprocess.run(
                [oracle_path], input=input_data, capture_output=True, timeout=1
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input of length {length}")

        try:
            agent_proc = subprocess.run(
                [agent_path], input=input_data, capture_output=True, timeout=1
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input of length {length}")

        assert agent_out == oracle_out, \
            f"Output mismatch on input of length {length}.\n" \
            f"Input (hex): {input_data.hex()}\n" \
            f"Oracle output: {oracle_out!r}\n" \
            f"Agent output: {agent_out!r}"

def test_monitor_script_exists():
    monitor_path = "/home/user/workspace/monitor.sh"
    assert os.path.isfile(monitor_path), f"{monitor_path} is missing"
    assert os.access(monitor_path, os.X_OK), f"{monitor_path} is not executable"

def test_bashrc_exported_variable():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} is missing"
    with open(bashrc_path, "r") as f:
        content = f.read()

    # Check if MONITOR_ACTIVE=1 is exported
    pattern = r"MONITOR_ACTIVE=1"
    assert re.search(pattern, content), \
        ".bashrc does not set MONITOR_ACTIVE=1"