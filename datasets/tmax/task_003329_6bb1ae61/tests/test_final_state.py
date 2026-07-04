# test_final_state.py

import os
import subprocess
import random
import base64
import string
import pytest

ORACLE_PATH = "/app/priv_checker"
AGENT_PATH = "/home/user/priv_checker.py"
N_TESTS = 1000

def generate_random_bytes(length):
    return bytes(random.getrandbits(8) for _ in range(length))

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation + ' ', k=length))

def generate_fuzz_inputs(n):
    random.seed(42)
    inputs = []

    # Edge cases
    inputs.append(None) # No arguments
    inputs.append("") # Empty argument

    for _ in range(n - 2):
        choice = random.random()
        if choice < 0.2:
            # Random bytes (might not be valid base64)
            length = random.randint(1, 1000)
            # Pass as raw string (which might contain null bytes, but we'll try to pass as argument)
            # To avoid subprocess issues with null bytes in args, we'll filter them out or encode properly.
            raw_bytes = generate_random_bytes(length).replace(b'\x00', b'\x01')
            try:
                inputs.append(raw_bytes.decode('utf-8', errors='surrogateescape'))
            except Exception:
                inputs.append(generate_random_string(length))
        elif choice < 0.4:
            # Valid base64 of random bytes
            length = random.randint(10, 500)
            raw_bytes = generate_random_bytes(length)
            inputs.append(base64.b64encode(raw_bytes).decode('ascii'))
        elif choice < 0.6:
            # Valid base64 of string with pipes
            length = random.randint(10, 500)
            s = generate_random_string(length) + "|" + generate_random_string(10) + "|" + generate_random_string(10)
            inputs.append(base64.b64encode(s.encode('utf-8')).decode('ascii'))
        elif choice < 0.8:
            # Valid base64 of almost correct format
            cert_sn = str(random.randint(0, 10))
            csp = "default-src 'none'" if random.random() > 0.5 else "default-src *"
            priv = random.choice(["root", "admin", "user", "guest"])
            s = f"{cert_sn}|{csp}|{priv}"
            inputs.append(base64.b64encode(s.encode('utf-8')).decode('ascii'))
        else:
            # Valid base64 of random string
            length = random.randint(10, 500)
            inputs.append(base64.b64encode(generate_random_string(length).encode('utf-8')).decode('ascii'))

    return inputs

def run_program(executable, arg):
    cmd = [executable]
    if arg is not None:
        cmd.append(arg)

    try:
        result = subprocess.run(cmd, capture_output=True, text=False, timeout=2)
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': b'',
            'stderr': b'Timeout',
            'returncode': -1
        }

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"

    inputs = generate_fuzz_inputs(N_TESTS)

    for i, arg in enumerate(inputs):
        oracle_res = run_program(ORACLE_PATH, arg)
        agent_res = run_program(AGENT_PATH, arg)

        error_msg = f"Mismatch on input #{i}: {repr(arg)}\n"
        error_msg += f"Oracle output: stdout={oracle_res['stdout']}, stderr={oracle_res['stderr']}, code={oracle_res['returncode']}\n"
        error_msg += f"Agent output: stdout={agent_res['stdout']}, stderr={agent_res['stderr']}, code={agent_res['returncode']}"

        assert oracle_res['returncode'] == agent_res['returncode'], error_msg
        assert oracle_res['stdout'] == agent_res['stdout'], error_msg
        assert oracle_res['stderr'] == agent_res['stderr'], error_msg