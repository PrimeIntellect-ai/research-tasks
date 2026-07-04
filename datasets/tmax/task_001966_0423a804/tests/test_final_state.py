# test_final_state.py

import os
import random
import string
import subprocess

def test_shared_library_exists():
    path = "/app/liburldecode/liburldecode.so"
    assert os.path.isfile(path), f"Shared library {path} was not built."

def test_api_file_exists():
    path = "/app/webhook_api.py"
    assert os.path.isfile(path), f"API file {path} was not created."

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/decode_cli"
    agent_path = "/app/liburldecode/decode_cli"

    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"

    random.seed(42)
    pool = string.ascii_letters + string.digits + string.punctuation + " "

    for _ in range(5000):
        length = random.randint(1, 500)
        chars = []
        for _ in range(length):
            if random.random() < 0.15:
                chars.append('%')
            else:
                chars.append(random.choice(pool))

        # Inject specific edge cases
        if random.random() < 0.05:
            chars.append('%')
        elif random.random() < 0.05:
            chars.extend(['%', random.choice(pool)])
        elif random.random() < 0.05:
            chars.extend(['%', random.choice(string.hexdigits), random.choice(pool)])

        test_str = "".join(chars)[:500]

        oracle_res = subprocess.run([oracle_path, test_str], capture_output=True)
        agent_res = subprocess.run([agent_path, test_str], capture_output=True)

        assert agent_res.returncode == oracle_res.returncode, (
            f"Exit code mismatch on input {repr(test_str)}.\n"
            f"Oracle exit code: {oracle_res.returncode}\n"
            f"Agent exit code: {agent_res.returncode}"
        )

        assert agent_res.stdout == oracle_res.stdout, (
            f"Output mismatch on input {repr(test_str)}.\n"
            f"Oracle stdout: {oracle_res.stdout!r}\n"
            f"Agent stdout: {agent_res.stdout!r}"
        )