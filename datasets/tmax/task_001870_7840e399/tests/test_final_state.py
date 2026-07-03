# test_final_state.py
import os
import random
import subprocess
import string

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + "./-_", k=length))

def generate_fuzz_input():
    # Using a slightly smaller max command count to ensure tests run within reasonable time limits
    num_commands = random.randint(0, 100)
    commands = []
    for _ in range(num_commands):
        cmd_type = random.choices(['WRITE', 'HLINK'], weights=[0.7, 0.3])[0]
        if cmd_type == 'WRITE':
            path = generate_random_string(random.randint(5, 80))
            size = random.randint(0, 4096)
            # using random bytes for data
            data = bytes(random.getrandbits(8) for _ in range(size))
            commands.append(f"WRITE {path} {size}\n".encode('utf-8') + data)
        else:
            target = generate_random_string(random.randint(5, 80))
            link = generate_random_string(random.randint(5, 80))
            commands.append(f"HLINK {target} {link}\n".encode('utf-8'))
    return b''.join(commands)

def test_fuzz_equivalence():
    agent_bin = "/home/user/archiver"
    oracle_bin = "/app/oracle_archiver"
    lock_file = "/tmp/fuzz_lock.lock"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    random.seed(42)

    for i in range(500):
        fuzz_input = generate_fuzz_input()

        oracle_proc = subprocess.run(
            [oracle_bin, lock_file],
            input=fuzz_input,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"

        agent_proc = subprocess.run(
            [agent_bin, lock_file],
            input=fuzz_input,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            assert False, f"Agent failed with return code {agent_proc.returncode} on input {i}.\nStderr: {agent_proc.stderr.decode('utf-8', errors='replace')}"

        if oracle_proc.stdout != agent_proc.stdout:
            assert False, f"Mismatch on input {i}. Agent output differs from Oracle output.\nOracle length: {len(oracle_proc.stdout)}, Agent length: {len(agent_proc.stdout)}"