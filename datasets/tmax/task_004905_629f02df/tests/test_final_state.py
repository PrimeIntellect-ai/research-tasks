# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

def test_users_json():
    users_file = "/home/user/pipeline/users.json"
    assert os.path.isfile(users_file), f"{users_file} does not exist."
    with open(users_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{users_file} is not valid JSON.")

    assert data.get("netadmin") == "netops", "User 'netadmin' is not mapped to 'netops' in users.json."
    assert data.get("backup_svc") == "backup", "User 'backup_svc' is not mapped to 'backup' in users.json."

def test_directories_created():
    backups_dir = "/home/user/pipeline/backups"
    logs_dir = "/home/user/pipeline/logs"
    assert os.path.isdir(backups_dir), f"Directory {backups_dir} was not created."
    assert os.path.isdir(logs_dir), f"Directory {logs_dir} was not created."

def test_pid_files_exist():
    flask_pid = "/home/user/pipeline/flask.pid"
    daemon_pid = "/home/user/pipeline/daemon.pid"
    assert os.path.isfile(flask_pid), f"Flask PID file {flask_pid} is missing."
    assert os.path.isfile(daemon_pid), f"Daemon PID file {daemon_pid} is missing."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_parser"
    agent_cmd = ["/usr/bin/python3", "/home/user/pipeline/parser_daemon.py", "--test-mode"]

    assert os.path.isfile(oracle_path), f"Oracle parser {oracle_path} missing."
    assert os.path.isfile(agent_cmd[1]), f"Agent parser {agent_cmd[1]} missing."

    random.seed(42)
    charset = string.ascii_letters + string.digits + ".:-_\n{}"

    for i in range(1000):
        length = random.randint(50, 500)
        inp = "".join(random.choices(charset, k=length))

        oracle_proc = subprocess.run(
            [oracle_path], 
            input=inp.encode('utf-8'), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(
            agent_cmd, 
            input=inp.encode('utf-8'), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            error_msg = (
                f"Mismatch found on random input #{i}!\n"
                f"Input:\n{inp}\n"
                f"Oracle Output:\n{oracle_out.decode('utf-8', errors='replace')}\n"
                f"Agent Output:\n{agent_out.decode('utf-8', errors='replace')}\n"
            )
            pytest.fail(error_msg)