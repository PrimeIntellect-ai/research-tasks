# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def test_sshd_config_hardened():
    config_path = "/home/user/sshd_config"
    assert os.path.exists(config_path), f"Missing SSH config file: {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    # Parse active configuration lines
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]

    # Check required SSH hardening directives
    assert "PasswordAuthentication no" in lines, "PasswordAuthentication is not set to 'no'"
    assert "HostKeyAlgorithms ssh-ed25519" in lines, "HostKeyAlgorithms is not restricted to 'ssh-ed25519'"

def test_keygen_fuzz_equivalence():
    oracle_path = "/app/keygen_legacy"
    agent_path = "/home/user/keygen_recreated.sh"

    assert os.path.exists(agent_path), f"Agent script missing at {agent_path}"

    # Generate fuzz inputs
    random.seed(42)
    charset = string.ascii_letters + string.digits

    env = os.environ.copy()
    env["ACTIVATION_PHRASE"] = "ds92"

    for _ in range(1000):
        length = random.randint(1, 64)
        fuzz_input = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path, fuzz_input],
            env=env,
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {fuzz_input}. Stderr: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["/bin/bash", agent_path, fuzz_input],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input: {fuzz_input}. Stderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on input '{fuzz_input}'. Oracle: '{oracle_out}', Agent: '{agent_out}'"