# test_final_state.py

import os
import stat
import subprocess
import random
import string
import binascii
import pytest

SSH_DIR = "/home/user/.ssh"
AUTH_KEYS_FILE = "/home/user/.ssh/authorized_keys"
AGENT_DECODER = "/home/user/decoder.py"
ORACLE_DECODER = "/app/oracle_decoder.py"

def test_ssh_permissions():
    """Verify that SSH directory and authorized_keys have secure permissions."""
    assert os.path.isdir(SSH_DIR), f"SSH directory missing at {SSH_DIR}"
    assert os.path.isfile(AUTH_KEYS_FILE), f"authorized_keys missing at {AUTH_KEYS_FILE}"

    dir_mode = stat.S_IMODE(os.stat(SSH_DIR).st_mode)
    file_mode = stat.S_IMODE(os.stat(AUTH_KEYS_FILE).st_mode)

    assert dir_mode == 0o700, f"Expected {SSH_DIR} permissions to be 700, got {oct(dir_mode)}"
    assert file_mode in (0o600, 0o644), f"Expected {AUTH_KEYS_FILE} permissions to be 600 or 644, got {oct(file_mode)}"

def test_backdoor_removed():
    """Verify that the backdoor key is removed and other keys remain."""
    with open(AUTH_KEYS_FILE, 'r') as f:
        lines = f.readlines()

    for line in lines:
        assert "hacker@c2-server" not in line, "Backdoor key 'hacker@c2-server' was not removed from authorized_keys"

    # Check that there are still keys left (setup had 3, 1 backdoor, so 2 should remain)
    valid_keys = [line for line in lines if line.strip() and not line.strip().startswith('#')]
    assert len(valid_keys) > 0, "All keys were removed from authorized_keys, expected legitimate keys to remain"

def test_decoder_exists():
    """Verify that the agent created the decoder script."""
    assert os.path.isfile(AGENT_DECODER), f"Agent decoder script missing at {AGENT_DECODER}"

def generate_fuzz_input(length):
    """Generate a random hex string representing ASCII text XORed with 170."""
    # Generate random ASCII text
    ascii_chars = string.ascii_letters + string.digits + string.punctuation + " "
    plain_text = ''.join(random.choice(ascii_chars) for _ in range(length))

    # XOR with 170
    obfuscated_bytes = bytes(ord(c) ^ 170 for c in plain_text)

    # Convert to hex
    return binascii.hexlify(obfuscated_bytes).decode('utf-8')

def test_decoder_fuzz_equivalence():
    """Fuzz the agent's decoder against the oracle."""
    assert os.path.isfile(ORACLE_DECODER), f"Oracle decoder missing at {ORACLE_DECODER}"

    random.seed(42)
    num_iterations = 100

    for i in range(num_iterations):
        # Lengths range from 5 to 100 bytes (10 to 200 hex chars)
        byte_length = random.randint(5, 100)
        hex_input = generate_fuzz_input(byte_length)

        # Run oracle
        oracle_proc = subprocess.run(
            ["python3", ORACLE_DECODER, hex_input],
            capture_output=True,
            text=True
        )
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["python3", AGENT_DECODER, hex_input],
            capture_output=True,
            text=True
        )
        agent_output = agent_proc.stdout

        assert agent_proc.returncode == 0, f"Agent decoder failed with return code {agent_proc.returncode} on input {hex_input}\nStderr: {agent_proc.stderr}"
        assert agent_output == oracle_output, f"Mismatch on input {hex_input}.\nExpected (Oracle): {repr(oracle_output)}\nGot (Agent): {repr(agent_output)}"