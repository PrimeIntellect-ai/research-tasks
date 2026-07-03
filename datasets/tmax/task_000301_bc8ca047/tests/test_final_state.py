# test_final_state.py
import os
import random
import string
import subprocess
import base64
import pytest

ORACLE_PATH = "/app/oracle_decoder"
AGENT_SCRIPT = "/home/user/decode_payload.py"
NUM_TESTS = 500

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_fuzz_inputs():
    random.seed(42)
    inputs = []
    for _ in range(NUM_TESTS):
        choice = random.randint(0, 3)
        if choice == 0:
            # Completely junk log line
            inputs.append(generate_random_string(50))
        elif choice == 1:
            # Valid format, random token, random serial
            token = base64.b64encode(os.urandom(32)).decode('utf-8')
            serial = "0x" + generate_random_string(6).upper()
            inputs.append(f'192.168.1.1 - - [10/Oct/2000:13:55:36 -0700] "GET /shell?token={token} HTTP/1.0" 200 2326 X-Client-Serial: {serial}')
        elif choice == 2:
            # Valid format, valid serial (e.g., 0x1A2B3C), random token
            token = base64.b64encode(os.urandom(32)).decode('utf-8')
            serial = "0x1A2B3C"
            inputs.append(f'192.168.1.1 - - [10/Oct/2000:13:55:36 -0700] "GET /shell?token={token} HTTP/1.0" 200 2326 X-Client-Serial: {serial}')
        else:
            # Valid format, valid serial, potentially valid token length (16 byte IV + 16 byte cipher)
            token = base64.b64encode(os.urandom(32)).decode('utf-8')
            serial = "0x1A2B3C"
            inputs.append(f'192.168.1.1 - - [10/Oct/2000:13:55:36 -0700] "GET /shell?token={token} HTTP/1.0" 200 2326 X-Client-Serial: {serial}')
    return inputs

@pytest.mark.parametrize("log_line", generate_fuzz_inputs())
def test_fuzz_equivalence(log_line):
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing: {AGENT_SCRIPT}"
    assert os.path.exists(ORACLE_PATH), f"Oracle missing: {ORACLE_PATH}"

    # Run oracle
    try:
        oracle_proc = subprocess.run(
            [ORACLE_PATH, log_line],
            capture_output=True,
            text=True,
            timeout=2
        )
        oracle_out = oracle_proc.stdout.strip()
    except subprocess.TimeoutExpired:
        oracle_out = "ORACLE_TIMEOUT"
    except Exception as e:
        oracle_out = f"ORACLE_ERROR: {e}"

    # Run agent
    try:
        agent_proc = subprocess.run(
            ["python3", AGENT_SCRIPT, log_line],
            capture_output=True,
            text=True,
            timeout=2
        )
        agent_out = agent_proc.stdout.strip()
    except subprocess.TimeoutExpired:
        agent_out = "AGENT_TIMEOUT"
    except Exception as e:
        agent_out = f"AGENT_ERROR: {e}"

    assert agent_out == oracle_out, f"Mismatch for input: {log_line}\nOracle: {oracle_out}\nAgent: {agent_out}"