# test_final_state.py

import os
import random
import subprocess
import pytest

def test_env_sh():
    env_path = "/home/user/env.sh"
    assert os.path.isfile(env_path), f"{env_path} does not exist"
    with open(env_path, "r") as f:
        content = f.read()

    # Check if TZ is exported correctly
    assert "TZ" in content and "Europe/Berlin" in content, f"{env_path} does not contain the correct TZ export"
    assert "export " in content, f"{env_path} does not export the variable"

def test_route_conf():
    route_path = "/home/user/route.conf"
    assert os.path.isfile(route_path), f"{route_path} does not exist"
    with open(route_path, "r") as f:
        content = f.read().strip()

    expected = "default via 192.168.1.1 dev eth1"
    assert content == expected, f"{route_path} content mismatch. Expected: '{expected}', Got: '{content}'"

def test_supervisor_sh():
    supervisor_path = "/home/user/supervisor.sh"
    assert os.path.isfile(supervisor_path), f"{supervisor_path} does not exist"
    assert os.access(supervisor_path, os.X_OK), f"{supervisor_path} is not executable"

    with open(supervisor_path, "r") as f:
        content = f.read()

    assert "env.sh" in content, "supervisor.sh does not source env.sh"
    assert "mkfifo" in content or "mknod" in content, "supervisor.sh does not create a named pipe"
    assert "sensor_data" in content, "supervisor.sh does not reference sensor_data"
    assert "while" in content or "until" in content, "supervisor.sh does not contain a loop"
    assert "processor" in content, "supervisor.sh does not run the processor"
    assert "processed.log" in content, "supervisor.sh does not append to processed.log"

def test_processor_fuzz_equivalence():
    agent_path = "/home/user/processor"
    oracle_path = "/app/oracle_processor"

    assert os.path.isfile(agent_path), f"Agent executable {agent_path} is missing"
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable"
    assert os.path.isfile(oracle_path), f"Oracle executable {oracle_path} is missing"
    assert os.access(oracle_path, os.X_OK), f"Oracle executable {oracle_path} is not executable"

    random.seed(42)
    iterations = 500

    for i in range(iterations):
        length = random.randint(1, 4096)
        input_data = bytes([random.randint(0, 255) for _ in range(length)])

        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle process timed out")

        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Agent process timed out")

        if agent_out != oracle_out:
            pytest.fail(
                f"Output mismatch on iteration {i}.\n"
                f"Input length: {length}\n"
                f"Oracle output length: {len(oracle_out)}\n"
                f"Agent output length: {len(agent_out)}\n"
                f"Oracle output (first 20 bytes): {oracle_out[:20]}\n"
                f"Agent output (first 20 bytes): {agent_out[:20]}"
            )