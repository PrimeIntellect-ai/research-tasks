# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_restore_mnt_and_fstab():
    mnt_path = "/home/user/restore_mnt"
    fstab_path = "/home/user/local_fstab"

    assert os.path.isdir(mnt_path), f"Directory {mnt_path} does not exist."
    assert os.path.isfile(os.path.join(mnt_path, "manifest.txt")), f"manifest.txt not found in {mnt_path}."

    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."
    with open(fstab_path, "r") as f:
        content = f.read()
    assert "/app/backup_data /home/user/restore_mnt none bind 0 0" in content, f"Expected bind mount entry not found in {fstab_path}."

def test_libnetconf_compiled():
    lib_path = "/app/libnetconf/libnetconf.a"
    assert os.path.isfile(lib_path), f"Static library {lib_path} was not successfully compiled."

def test_processed_manifest():
    processed_path = "/home/user/processed_manifest.txt"
    assert os.path.isfile(processed_path), f"Processed manifest {processed_path} does not exist."

    with open(processed_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            assert parts[2] == "RESTORED", f"Found line where 3rd column is not 'RESTORED': {line}"

def test_ssh_tunnel_cmd():
    cmd_path = "/home/user/ssh_tunnel_cmd.txt"
    assert os.path.isfile(cmd_path), f"SSH command file {cmd_path} does not exist."

    with open(cmd_path, "r") as f:
        content = f.read().strip()

    # Check for ssh command and forwarding flags
    assert content.startswith("ssh"), "Command does not start with 'ssh'"
    assert "9090" in content, "Local port 9090 not found in SSH command"
    assert "8080" in content, "Remote port 8080 not found in SSH command"

def test_fuzz_equivalence_validate_ip_format():
    oracle_path = "/opt/oracle/validate_ip_format_oracle"
    agent_path = "/home/user/validate_ip_format"

    assert os.path.isfile(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary not executable at {oracle_path}"

    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary not executable at {agent_path}"

    random.seed(42)
    charset = string.ascii_letters + string.digits + ".:_- "

    # Generate random inputs
    inputs = []
    for _ in range(10000):
        length = random.randint(5, 50)
        inp = "".join(random.choices(charset, k=length))
        inputs.append(inp)

    # Also include some inputs that are likely to be valid or close to valid
    inputs.append("ROUTE:1234.A")
    inputs.append("ROUTE:123.A")
    inputs.append("ROUTE:12345.A")
    inputs.append("ROUTE:1234.a")
    inputs.append("ROUTE:1234.AB")
    inputs.append("ROUTE:1234.B")

    for inp in inputs:
        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=inp.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=1
            )
            oracle_out = oracle_proc.stdout.decode('utf-8')
        except Exception as e:
            pytest.fail(f"Oracle failed to run on input {repr(inp)}: {e}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=inp.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=1
            )
            agent_out = agent_proc.stdout.decode('utf-8')
        except Exception as e:
            pytest.fail(f"Agent failed to run on input {repr(inp)}: {e}")

        assert oracle_out == agent_out, (
            f"Output mismatch on input {repr(inp)}.\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output: {repr(agent_out)}"
        )