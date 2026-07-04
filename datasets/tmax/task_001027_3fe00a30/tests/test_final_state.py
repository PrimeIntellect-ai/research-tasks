# test_final_state.py
import os
import subprocess
import random
import string
import tempfile
import pytest

def generate_random_path():
    length = random.randint(5, 30)
    chars = string.ascii_letters + string.digits + "/."
    path = "".join(random.choice(chars) for _ in range(length))
    if random.random() < 0.1:
        path += ".tmp"
    return path

def generate_random_checksum():
    if random.random() < 0.05:
        return 0
    return random.randint(1, 4294967295)

def generate_manifest(num_lines, path_pool):
    lines = []
    for _ in range(num_lines):
        path = random.choice(path_pool)
        cs = generate_random_checksum()
        lines.append(f"{path}\t{cs}\n")
    return "".join(lines)

def test_fuzz_equivalence():
    agent_bin = "/home/user/diff_tool"
    oracle_bin = "/app/oracle_diff_tool"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    random.seed(42)

    for i in range(100):
        num_old = random.randint(0, 1000)
        num_new = random.randint(0, 1000)

        # Create a pool of paths to ensure high overlap between old and new manifests
        pool_size = max(10, (num_old + num_new) // 2)
        path_pool = [generate_random_path() for _ in range(pool_size)]

        old_manifest = generate_manifest(num_old, path_pool)
        new_manifest = generate_manifest(num_new, path_pool)

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f_new:
            f_new.write(new_manifest)
            new_manifest_path = f_new.name

        try:
            oracle_proc = subprocess.run(
                [oracle_bin, new_manifest_path],
                input=old_manifest,
                text=True,
                capture_output=True
            )

            agent_proc = subprocess.run(
                [agent_bin, new_manifest_path],
                input=old_manifest,
                text=True,
                capture_output=True
            )

            assert agent_proc.stdout == oracle_proc.stdout, (
                f"Output mismatch on fuzz iteration {i}.\n\n"
                f"Oracle output:\n{oracle_proc.stdout}\n\n"
                f"Agent output:\n{agent_proc.stdout}\n"
            )
        finally:
            os.remove(new_manifest_path)