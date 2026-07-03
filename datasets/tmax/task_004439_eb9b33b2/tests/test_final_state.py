# test_final_state.py

import os
import stat
import subprocess
import random
import pytest

def test_rogue_service_terminated():
    """Verify that no service is listening on a TCP port between 8000 and 9000."""
    try:
        output = subprocess.check_output(['ss', '-tln']).decode()
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute 'ss' command to check listening ports.")

    for port in range(8000, 9001):
        # Look for the port in the output. 'ss' output usually looks like:
        # LISTEN 0 128 0.0.0.0:8000 0.0.0.0:*
        if f":{port} " in output or f":{port}\t" in output or f":{port}\n" in output:
            pytest.fail(f"Rogue service is still listening on port {port}.")

def test_suid_backdoor_fixed():
    """Verify that the SUID permission is removed from the backdoor binary."""
    path = "/var/tmp/.backdoor"
    if os.path.exists(path):
        st = os.stat(path)
        assert not (st.st_mode & stat.S_ISUID), f"File {path} still has SUID permission set."
    # If it was deleted completely, that's also an acceptable remediation.

def test_sshd_config_secured():
    """Verify that PermitRootLogin is not set to 'yes' in sshd_config."""
    path = "/etc/ssh/sshd_config"
    assert os.path.isfile(path), f"SSH config not found at {path}."

    with open(path, 'r') as f:
        lines = f.readlines()

    vulnerable = False
    for line in lines:
        line = line.strip()
        # Ignore comments
        if line.startswith("#"):
            continue
        # Check for PermitRootLogin yes
        if line.startswith("PermitRootLogin") and "yes" in line:
            vulnerable = True
            break

    assert not vulnerable, f"Vulnerable 'PermitRootLogin yes' configuration is still active in {path}."

def test_decryptor_fuzz_equivalence():
    """Verify that the agent's decryptor behaves exactly like the oracle decryptor on random inputs."""
    oracle_path = "/app/oracle_decryptor"
    agent_path = "/home/user/decryptor"

    assert os.path.isfile(oracle_path), f"Oracle decryptor missing at {oracle_path}."
    assert os.access(oracle_path, os.X_OK), f"Oracle decryptor at {oracle_path} is not executable."

    assert os.path.isfile(agent_path), f"Agent decryptor missing at {agent_path}."
    assert os.access(agent_path, os.X_OK), f"Agent decryptor at {agent_path} is not executable."

    random.seed(42)
    num_tests = 500

    for i in range(num_tests):
        # Generate random byte stream of length 1 to 8192
        length = random.randint(1, 8192)
        fuzz_input = bytes(random.choices(range(256), k=length))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=fuzz_input,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2,
                check=True
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle decryptor timed out.")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle decryptor failed with exit code {e.returncode}.")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=fuzz_input,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2,
                check=False
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent decryptor timed out on input of length {length}.")

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent decryptor failed with exit code {agent_proc.returncode}.")

        if agent_out != oracle_out:
            # Provide a truncated hex dump for debugging if it mismatches
            input_hex = fuzz_input[:32].hex() + ("..." if len(fuzz_input) > 32 else "")
            oracle_hex = oracle_out[:32].hex() + ("..." if len(oracle_out) > 32 else "")
            agent_hex = agent_out[:32].hex() + ("..." if len(agent_out) > 32 else "")
            pytest.fail(
                f"Mismatch on fuzz iteration {i+1} (input length {length}).\n"
                f"Input (hex): {input_hex}\n"
                f"Expected output (hex): {oracle_hex}\n"
                f"Agent output (hex): {agent_hex}"
            )