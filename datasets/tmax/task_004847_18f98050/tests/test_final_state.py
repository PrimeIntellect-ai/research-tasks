# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_provision_directory_and_symlink():
    instance_id = "vm-alpha-88"
    dir_path = f"/home/user/provision/{instance_id}"
    symlink_path = os.path.join(dir_path, "latest-disk")

    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    assert target == "/app/base.qcow2", f"Symlink {symlink_path} points to {target}, expected /app/base.qcow2"

def test_ssh_tunnel_pid():
    pid_file = "/home/user/tunnel.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from {pid_file} is not running.")

    # Check if it's an ssh process (optional but good)
    try:
        cmdline = open(f"/proc/{pid}/cmdline", "r").read().replace('\x00', ' ')
        assert "ssh" in cmdline, f"Process {pid} is not an ssh command: {cmdline}"
        assert "8080:localhost:9922" in cmdline or "8080:127.0.0.1:9922" in cmdline, f"SSH command does not contain the correct port forwarding: {cmdline}"
    except FileNotFoundError:
        pass

def test_proxy_filter_fuzz_equivalence():
    agent_bin = "/home/user/proxy_filter"
    oracle_bin = "/app/reference_proxy_filter"

    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} does not exist."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable."

    random.seed(42)
    charset = string.ascii_letters + string.digits

    def generate_input():
        length = random.randint(10, 100)
        chars = [random.choice(charset) for _ in range(length)]
        # Ensure "DEV" is present
        insert_pos = random.randint(0, max(0, length - 3))
        chars[insert_pos:insert_pos+3] = list("DEV")
        # Maybe add multiple "DEV"s
        if random.random() > 0.5:
            insert_pos2 = random.randint(0, max(0, len(chars) - 3))
            chars[insert_pos2:insert_pos2+3] = list("DEV")
        return "".join(chars) + "\n"

    inputs = [generate_input() for _ in range(1000)]
    input_data = "".join(inputs).encode("utf-8")

    agent_proc = subprocess.run([agent_bin], input=input_data, capture_output=True)
    oracle_proc = subprocess.run([oracle_bin], input=input_data, capture_output=True)

    assert agent_proc.returncode == 0, f"Agent binary failed with return code {agent_proc.returncode}\nStderr: {agent_proc.stderr.decode()}"
    assert oracle_proc.returncode == 0, f"Oracle binary failed with return code {oracle_proc.returncode}"

    agent_out = agent_proc.stdout.decode("utf-8").splitlines()
    oracle_out = oracle_proc.stdout.decode("utf-8").splitlines()

    assert len(agent_out) == len(oracle_out), f"Output line count mismatch: agent={len(agent_out)}, oracle={len(oracle_out)}"

    for i, (a_line, o_line) in enumerate(zip(agent_out, oracle_out)):
        if a_line != o_line:
            orig_input = inputs[i].strip()
            pytest.fail(f"Mismatch on input line {i+1}: '{orig_input}'\nExpected: '{o_line}'\nGot:      '{a_line}'")