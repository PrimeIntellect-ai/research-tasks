# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def test_squashfuse_mounted():
    mount_point = "/home/user/data_mount"
    assert os.path.ismount(mount_point), f"{mount_point} is not a mount point. Did you mount the squashfs image?"

    with open("/proc/mounts", "r") as f:
        mounts = f.read()

    # Check if the mount point is associated with fuse/squashfuse
    is_squashfuse = False
    for line in mounts.splitlines():
        if mount_point in line and ("fuse" in line or "squashfuse" in line):
            is_squashfuse = True
            break

    assert is_squashfuse, f"Expected {mount_point} to be mounted using squashfuse."

def test_socat_running():
    try:
        ps_output = subprocess.check_output(["ps", "aux"]).decode()
        assert "socat" in ps_output, "socat is not running."
        # The exact command might vary, but it must involve 9090 and 8080
        assert "9090" in ps_output and "8080" in ps_output, "socat does not appear to be forwarding port 9090 to 8080."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps to check running processes.")

def test_crontab():
    try:
        crontab_output = subprocess.check_output(["crontab", "-l"]).decode()
        assert "*/5 * * * *" in crontab_output, "Crontab missing the '*/5 * * * *' schedule."
        assert "/home/user/parser" in crontab_output, "Crontab is missing the command '/home/user/parser'."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Did you add the scheduled task?")

def test_parser_fuzzing():
    oracle = "/app/oracle_parser"
    agent = "/home/user/parser"

    assert os.path.exists(agent), f"Agent executable {agent} not found. Did you compile it?"
    assert os.access(agent, os.X_OK), f"Agent executable {agent} is not executable."

    random.seed(42)

    inputs = []
    for _ in range(10000):
        choice = random.random()
        if choice < 0.7:
            # Valid format
            dev = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 8)))
            used = random.randint(0, 100000)
            total = random.randint(0, 100000)
            inputs.append(f"{dev} {used} {total}")
        elif choice < 0.8:
            # Invalid numbers
            dev = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 8)))
            inputs.append(f"{dev} abc def")
        elif choice < 0.9:
            # Missing fields
            dev = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 8)))
            inputs.append(f"{dev} {random.randint(0, 100000)}")
        else:
            # Random garbage
            # Strip newlines to keep it single-line per input
            garbage = ''.join(random.choices(string.printable, k=random.randint(1, 50))).replace('\n', ' ')
            inputs.append(garbage)

    input_data = "\n".join(inputs) + "\n"

    oracle_proc = subprocess.run([oracle], input=input_data, text=True, capture_output=True)
    agent_proc = subprocess.run([agent], input=input_data, text=True, capture_output=True)

    assert agent_proc.returncode == oracle_proc.returncode, f"Exit codes do not match. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

    oracle_lines = oracle_proc.stdout.splitlines()
    agent_lines = agent_proc.stdout.splitlines()

    if len(agent_lines) != len(oracle_lines):
        pytest.fail(f"Output line counts do not match. Oracle produced {len(oracle_lines)} lines, Agent produced {len(agent_lines)} lines.")

    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert o_line == a_line, f"Mismatch at output line {i+1}:\nOracle: {o_line}\nAgent:  {a_line}"