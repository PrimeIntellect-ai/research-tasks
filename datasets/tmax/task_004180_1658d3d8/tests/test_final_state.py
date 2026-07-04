# test_final_state.py

import os
import stat
import random
import subprocess
import configparser
import grp
import pwd

def test_user_and_group():
    # Check group
    try:
        group_info = grp.getgrnam("archive_grp")
    except KeyError:
        assert False, "Group 'archive_grp' does not exist."

    # Check user
    try:
        user_info = pwd.getpwnam("archive_usr")
    except KeyError:
        assert False, "User 'archive_usr' does not exist."

    # Check user is in group
    user_groups = [g.gr_name for g in grp.getgrall() if user_info.pw_name in g.gr_mem]
    if group_info.gr_name not in user_groups and user_info.pw_gid != group_info.gr_gid:
        assert False, f"User 'archive_usr' is not a member of 'archive_grp'."

def test_fuzz_equivalence_obfuscator():
    oracle_path = "/app/oracle/obfuscator_oracle"
    agent_path = "/home/user/obfuscator"

    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)

    for i in range(500):
        length = random.randint(0, 1024)
        input_data = bytes(random.getrandbits(8) for _ in range(length))

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        assert oracle_proc.returncode == 0, "Oracle failed to execute"
        oracle_output = oracle_proc.stdout

        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)
        assert agent_proc.returncode == 0, f"Agent binary failed to execute on iteration {i}"
        agent_output = agent_proc.stdout

        assert oracle_output == agent_output, (
            f"Output mismatch on iteration {i}.\n"
            f"Input length: {length}\n"
            f"Oracle output length: {len(oracle_output)}\n"
            f"Agent output length: {len(agent_output)}\n"
        )

def test_supervisord_config():
    config_path = "/home/user/supervisord.conf"
    assert os.path.exists(config_path), f"Config file not found at {config_path}"

    config = configparser.ConfigParser()
    try:
        config.read(config_path)
    except Exception as e:
        assert False, f"Failed to parse {config_path}: {e}"

    # check redis
    assert "program:redis" in config.sections(), "Missing [program:redis] section"
    redis_cmd = config.get("program:redis", "command", fallback="")
    assert "redis-server" in redis_cmd and "6379" in redis_cmd, "redis command is incorrect"

    # check smtp_receiver
    assert "program:smtp_receiver" in config.sections(), "Missing [program:smtp_receiver] section"
    smtp_cmd = config.get("program:smtp_receiver", "command", fallback="")
    assert "smtp_receiver.py" in smtp_cmd, "smtp_receiver command is incorrect"
    assert config.get("program:smtp_receiver", "user", fallback="") == "archive_usr", "smtp_receiver user is not archive_usr"

    # check archive_worker
    assert "program:archive_worker" in config.sections(), "Missing [program:archive_worker] section"
    worker_cmd = config.get("program:archive_worker", "command", fallback="")
    assert "archive_worker.py" in worker_cmd, "archive_worker command is incorrect"
    assert config.get("program:archive_worker", "user", fallback="") == "archive_usr", "archive_worker user is not archive_usr"

    env_str = config.get("program:archive_worker", "environment", fallback="")
    assert "OBFUSCATOR_BIN" in env_str and "/home/user/obfuscator" in env_str, "archive_worker environment missing OBFUSCATOR_BIN"

def test_rollout_script():
    script_path = "/home/user/rollout.sh"
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

    with open(script_path, "r") as f:
        content = f.read()

    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]

    # Needs to restart archive_worker, sleep 2, restart smtp_receiver in that order
    worker_idx = -1
    sleep_idx = -1
    smtp_idx = -1

    for i, line in enumerate(lines):
        if "supervisorctl" in line and "restart" in line and "archive_worker" in line:
            worker_idx = i
        elif "sleep 2" in line or "sleep  2" in line:
            sleep_idx = i
        elif "supervisorctl" in line and "restart" in line and "smtp_receiver" in line:
            smtp_idx = i

    assert worker_idx != -1, "Script missing supervisorctl restart archive_worker"
    assert sleep_idx != -1, "Script missing sleep 2"
    assert smtp_idx != -1, "Script missing supervisorctl restart smtp_receiver"

    assert worker_idx < sleep_idx < smtp_idx, "Commands in rollout.sh are not in the correct order"