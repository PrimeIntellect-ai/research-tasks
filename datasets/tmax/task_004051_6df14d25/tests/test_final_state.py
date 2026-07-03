# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/log_auditor"
AGENT_SCRIPT = "/home/user/emulator.py"

def generate_test_cases(n=1000):
    random.seed(42)
    cases = []
    chars = string.ascii_letters + string.digits + string.punctuation

    for _ in range(n):
        # Generate CSP
        csp_length = random.randint(10, 50)
        csp = ''.join(random.choice(chars) for _ in range(csp_length))
        if random.random() < 0.3:
            csp += " script-src 'self'"

        # Generate payload plaintext
        payload_length = random.randint(5, 100)
        payload_bytes = bytearray(random.getrandbits(8) for _ in range(payload_length))

        # Occasionally inject SSN into plaintext
        if random.random() < 0.3 and payload_length >= 11:
            ssn_str = f"{random.randint(100,999):03d}-{random.randint(10,99):02d}-{random.randint(1000,9999):04d}"
            ssn_bytes = ssn_str.encode('ascii')
            insert_idx = random.randint(0, payload_length - len(ssn_bytes))
            payload_bytes[insert_idx:insert_idx+len(ssn_bytes)] = ssn_bytes

        # Encrypt the payload bytes to create the input hex
        S = 0x5A
        ciphertext = bytearray()
        for b in payload_bytes:
            S = (S * 31 + 17) & 0xFF
            K = S
            ciphertext.append(b ^ K)

        payload_hex = ciphertext.hex()
        input_str = f"CSP: {csp} | PAYLOAD: {payload_hex}\n"
        cases.append(input_str)

    return cases

def run_program(cmd, input_str):
    result = subprocess.run(
        cmd,
        input=input_str,
        text=True,
        capture_output=True,
        timeout=2
    )
    return result.stdout

def test_emulator_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

    test_cases = generate_test_cases(1000)

    for i, input_str in enumerate(test_cases):
        oracle_out = run_program([ORACLE_PATH], input_str)
        agent_out = run_program(["python3", AGENT_SCRIPT], input_str)

        assert oracle_out == agent_out, (
            f"Output mismatch on test case {i+1}:\n"
            f"Input:\n{input_str}\n"
            f"Oracle Output:\n{oracle_out}\n"
            f"Agent Output:\n{agent_out}\n"
        )