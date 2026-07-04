# test_final_state.py

import os
import random
import subprocess
import struct
import hmac
import hashlib
import pytest

ORACLE_PATH = "/app/oracle_bin"
AGENT_SCRIPT = "/home/user/redirect_handler.py"
SECRET_KEY = b"5938210476"

def generate_random_hex(length):
    return bytes(random.getrandbits(8) for _ in range(length)).hex()

def generate_token(url, key=SECRET_KEY, corrupt_magic=False, corrupt_length=False, corrupt_hmac=False):
    magic = b"REDI" if not corrupt_magic else b"R3DI"
    url_bytes = url.encode('ascii', errors='ignore')
    length = len(url_bytes)

    if corrupt_length:
        length_field = struct.pack(">H", (length + 1) % 65536)
    else:
        length_field = struct.pack(">H", length)

    data = magic + length_field + url_bytes
    sig = hmac.new(key, data, hashlib.sha256).digest()

    if corrupt_hmac:
        sig = bytearray(sig)
        sig[0] ^= 0xFF
        sig = bytes(sig)

    return (data + sig).hex()

def generate_inputs(n=10000):
    random.seed(42)
    inputs = []

    for _ in range(n // 5):
        # 1. Completely random hex strings
        length = random.randint(0, 150)
        inputs.append(generate_random_hex(length))

        # 2. Valid magic REDI but random lengths/data (format error)
        url = "https://example.com/" + "".join(chr(random.randint(32, 126)) for _ in range(random.randint(5, 20)))
        inputs.append(generate_token(url, corrupt_length=True))

        # 3. Valid structure but invalid HMAC
        url = "https://secure.internal/" + "".join(chr(random.randint(97, 122)) for _ in range(random.randint(5, 20)))
        inputs.append(generate_token(url, corrupt_hmac=True))

        # 4. Valid structure and HMAC, but violate URL policy
        bad_urls = [
            "http://secure.internal/admin",
            "https://secure.internal/admin?user=1",
            "https://secure.internal/admin@domain",
            "https://secure.internal/admin//dashboard",
            "https://attacker.com/"
        ]
        inputs.append(generate_token(random.choice(bad_urls)))

        # 5. Perfectly valid and safe tokens
        url = "https://secure.internal/" + "".join(chr(random.randint(97, 122)) for _ in range(random.randint(5, 20)))
        inputs.append(generate_token(url))

    return inputs

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"

    inputs = generate_inputs(2000) # Reduced to 2000 to avoid test timeouts, while maintaining coverage

    for i, hex_input in enumerate(inputs):
        oracle_proc = subprocess.run(
            [ORACLE_PATH, hex_input],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_proc.stdout.strip()

        agent_proc = subprocess.run(
            ["python3", AGENT_SCRIPT, hex_input],
            capture_output=True,
            text=True
        )
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input {i} ({hex_input[:30]}...):\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}"
        )