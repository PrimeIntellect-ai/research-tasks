# test_final_state.py

import os
import stat
import subprocess
import random
import pytest

def test_fuzz_equivalence_sec_logger():
    oracle_path = "/app/sec_logger"
    agent_path = "/home/user/sec_logger_clone"

    assert os.path.exists(agent_path), f"Agent binary {agent_path} does not exist."
    assert os.path.isfile(agent_path), f"{agent_path} is not a file."
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable."

    random.seed(42)
    for i in range(100): # 100 iterations is sufficient for fuzzing this simple behavior
        length = random.randint(1, 4096)
        input_data = bytes(random.getrandbits(8) for _ in range(length))

        oracle_proc = subprocess.run(
            [oracle_path], input=input_data, capture_output=True, timeout=2
        )
        agent_proc = subprocess.run(
            [agent_path], input=input_data, capture_output=True, timeout=2
        )

        assert oracle_proc.returncode == agent_proc.returncode, f"Return code mismatch on iteration {i}"
        assert oracle_proc.stdout == agent_proc.stdout, f"Output mismatch on iteration {i} for input length {length}"

def test_expect_script_and_auth():
    expect_script = "/home/user/init.exp"
    conf_file = "/home/user/logger.conf"

    assert os.path.exists(expect_script), f"Expect script {expect_script} does not exist."
    assert os.path.exists(conf_file), f"Configuration file {conf_file} does not exist."

    with open(conf_file, "r") as f:
        content = f.read().strip()

    assert "AUTH_OK=1" in content, f"Configuration file {conf_file} does not contain expected AUTH_OK=1. Was the expect script run correctly?"

def test_supervisor_and_fifo():
    supervisor_script = "/home/user/supervisor.sh"
    fifo_path = "/home/user/input.fifo"

    assert os.path.exists(supervisor_script), f"Supervisor script {supervisor_script} does not exist."
    assert os.access(supervisor_script, os.X_OK), f"Supervisor script {supervisor_script} is not executable."

    assert os.path.exists(fifo_path), f"FIFO {fifo_path} does not exist."
    assert stat.S_ISFIFO(os.stat(fifo_path).st_mode), f"{fifo_path} is not a named pipe (FIFO)."

def test_logrotate_config():
    logrotate_conf = "/home/user/logrotate.conf"
    assert os.path.exists(logrotate_conf), f"logrotate configuration {logrotate_conf} does not exist."

    with open(logrotate_conf, "r") as f:
        content = f.read()

    assert "/home/user/logs/output.log" in content, "logrotate.conf does not target /home/user/logs/output.log"

    directives = ["daily", "rotate 7", "compress", "missingok", "size 10k"]
    for directive in directives:
        # Simple check for required directives. We remove extra spaces to be robust.
        assert directive.replace(" ", "") in content.replace(" ", "").replace("\t", ""), f"logrotate.conf is missing or has incorrect directive related to: {directive}"