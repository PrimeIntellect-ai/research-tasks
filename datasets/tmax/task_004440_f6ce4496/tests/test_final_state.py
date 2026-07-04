# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def encrypt(plaintext: str) -> str:
    key = [0x4B, 0x1D, 0x9A, 0xF2]
    ciphertext = []
    for i, char in enumerate(plaintext):
        p = ord(char)
        c = ((p ^ key[i % 4]) + (i * 3)) % 256
        ciphertext.append(f"{c:02x}")
    return "".join(ciphertext)

def test_fuzz_equivalence():
    oracle_path = "/app/reference_crypto"
    agent_path = "/home/user/decryptor"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable at {oracle_path}"

    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary not executable at {agent_path}"

    random.seed(42)
    printable_chars = string.ascii_letters + string.digits + string.punctuation + " "

    for _ in range(200):
        length = random.randint(1, 250)
        plaintext = "".join(random.choice(printable_chars) for _ in range(length))
        hex_input = encrypt(plaintext)

        try:
            oracle_res = subprocess.run([oracle_path, hex_input], capture_output=True, text=True, timeout=2)
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {hex_input}")

        try:
            agent_res = subprocess.run([agent_path, hex_input], capture_output=True, text=True, timeout=2)
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on input {hex_input}")

        assert agent_res.stdout == oracle_res.stdout, (
            f"Output mismatch on input {hex_input}.\n"
            f"Expected (Oracle): {repr(oracle_res.stdout)}\n"
            f"Got (Agent): {repr(agent_res.stdout)}"
        )