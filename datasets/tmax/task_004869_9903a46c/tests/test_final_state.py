# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

AGENT_BIN = "/home/user/secure_rotator"
ORACLE_BIN = "/app/oracle_rotator"
N_TESTS = 5000

def generate_random_string(min_len, max_len, chars):
    return ''.join(random.choice(chars) for _ in range(random.randint(min_len, max_len)))

def generate_passwd_file(num_lines):
    lines = []
    for _ in range(num_lines):
        user = generate_random_string(3, 8, string.ascii_lowercase)
        pwd = generate_random_string(64, 64, string.hexdigits.lower())
        uid = random.randint(1000, 9999)
        gid = random.randint(1000, 9999)
        gecos = generate_random_string(5, 15, string.ascii_letters)
        home = f"/home/{user}"
        shell = random.choice(["/bin/bash", "/bin/sh", "/bin/false"])
        lines.append(f"{user}:{pwd}:{uid}:{gid}:{gecos}:{home}:{shell}")
    if not lines:
        return ""
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary is not executable: {AGENT_BIN}"
    assert os.path.isfile(ORACLE_BIN), f"Oracle binary not found at {ORACLE_BIN}"

    random.seed(42)

    for i in range(N_TESTS):
        arg1 = generate_random_string(1, 32, string.ascii_letters + string.digits)
        arg2 = generate_random_string(64, 64, string.hexdigits.lower())

        num_lines = random.randint(0, 20)
        stdin_content = generate_passwd_file(num_lines)

        # Sometimes ensure the targeted user actually exists in the file
        if random.random() < 0.5 and num_lines > 0:
            lines = stdin_content.strip().split('\n')
            target_line = random.choice(lines)
            arg1 = target_line.split(':')[0]

        perms = random.choice([0o600, 0o644])

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tf:
            tf.write(stdin_content)
            tf.flush()
            temp_name = tf.name

        try:
            os.chmod(temp_name, perms)

            with open(temp_name, 'r') as f_agent, open(temp_name, 'r') as f_oracle:
                proc_agent = subprocess.run(
                    [AGENT_BIN, arg1, arg2],
                    stdin=f_agent,
                    capture_output=True,
                    text=True
                )
                proc_oracle = subprocess.run(
                    [ORACLE_BIN, arg1, arg2],
                    stdin=f_oracle,
                    capture_output=True,
                    text=True
                )

            assert proc_agent.returncode == proc_oracle.returncode, (
                f"Return code mismatch on test {i}.\n"
                f"Args: {arg1} {arg2}, Perms: {oct(perms)}\n"
                f"Oracle: {proc_oracle.returncode}, Agent: {proc_agent.returncode}\n"
                f"Oracle stderr: {proc_oracle.stderr}\nAgent stderr: {proc_agent.stderr}"
            )
            assert proc_agent.stdout == proc_oracle.stdout, (
                f"Stdout mismatch on test {i}.\n"
                f"Args: {arg1} {arg2}, Perms: {oct(perms)}\n"
                f"Oracle stdout: {proc_oracle.stdout}\nAgent stdout: {proc_agent.stdout}"
            )
            assert proc_agent.stderr == proc_oracle.stderr, (
                f"Stderr mismatch on test {i}.\n"
                f"Args: {arg1} {arg2}, Perms: {oct(perms)}\n"
                f"Oracle stderr: {proc_oracle.stderr}\nAgent stderr: {proc_agent.stderr}"
            )
        finally:
            os.remove(temp_name)